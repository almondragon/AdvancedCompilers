#include "llvm/IR/Function.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Analysis/MemorySSA.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/FileSystem.h" // added to generate a graphical view

using namespace llvm;

void writeMemorySSADot(Function &F, MemorySSA &MSSA) {
    // preparing the DOT file for the graph
    std::error_code EC;
    std::string FileName = F.getName().str() + "_MemorySSA.dot";
    raw_fd_ostream File(FileName, EC, sys::fs::OF_Text);

    if (EC){
      errs() << "Error opening file " << FileName << ": " << EC.message() << "\n";
      return;
    }

    // doing the header for the graph
    File << "digraph MemorySSA_" << F.getName() << " {\n";
    File << " node [shape=box, style=filled, fillcolor=lightblue];\n";

    // iterate over memory access
    for (auto &BB : F) {
        for (auto &I : BB) {
            if (auto *MA = MSSA.getMemoryAccess(&I)) {
                std::string NodeName;
                raw_string_ostream NodeStream(NodeName);
                MA->print(NodeStream);
                NodeStream.flush();

                // sanitize quotes
                for (auto &c : NodeName) if (c == '"') c = '\'';

                File << "  \"" << (void*)MA << "\" [label=\"" << NodeName << "\"];\n";

                // draw edge to defining access
                if (auto *Def = MA->getDefiningAccess()) {
                    File << "  \"" << (void*)Def << "\" -> \"" << (void*)MA << "\";\n";
                }
            }
        }

        // Handle MemoryPhi at block entry
        if (auto *Phi = MSSA.getMemoryAccess(&BB)) {
            if (auto *MPhi = dyn_cast<MemoryPhi>(Phi)) {
                std::string PhiName;
                raw_string_ostream PhiStream(PhiName);
                MPhi->print(PhiStream);
                PhiStream.flush();
                for (auto &c : PhiName) if (c == '"') c = '\'';

                File << "  \"" << (void*)MPhi << "\" [label=\"" << PhiName << "\", shape=diamond];\n";

                // incoming edges
                for (unsigned i = 0; i < MPhi->getNumIncomingValues(); ++i) {
                    auto *IncomingAcc = MPhi->getIncomingValue(i);
                    File << "  \"" << (void*)IncomingAcc << "\" -> \"" << (void*)MPhi << "\";\n";
                }
            }
        }
    }

    File << "}\n";

    errs() << "MemorySSA graph written to " << FileName << "\n";
}

struct MemorySSADemoPass : PassInfoMixin<MemorySSADemoPass> {
  PreservedAnalyses run(Function &F, FunctionAnalysisManager &AM) {
    auto &MSSAResult = AM.getResult<MemorySSAAnalysis>(F);
    auto &MSSA = MSSAResult.getMSSA();

    errs() << "Analyzing function: " << F.getName() << "\n";

    // Iterate over basic blocks to show all MemoryAccesses
    for (auto &BB : F) {
      errs() << "BasicBlock: " << BB.getName() << "\n";

      // MemoryPhi nodes are found at block entries
      if (auto *Phi = MSSA.getMemoryAccess(&BB)) {
        if (auto *MPhi = dyn_cast<MemoryPhi>(Phi)) {
          errs() << "  MemoryPhi for block " << BB.getName() << ":\n";
          for (unsigned i = 0; i < MPhi->getNumIncomingValues(); ++i) {
            auto *IncomingAcc = MPhi->getIncomingValue(i);
            auto *Pred = MPhi->getIncomingBlock(i);
            errs() << "    from " << Pred->getName() << ": ";
            IncomingAcc->print(errs());
            errs() << "\n";
          }
        }
      }

      // Iterate over instructions for MemoryDef/Use
      for (auto &I : BB) {
        if (auto *MA = MSSA.getMemoryAccess(&I)) {
          errs() << "  ";
          MA->print(errs());
          errs() << "\n";
        }
      }
    }

    // call helper

    writeMemorySSADot(F, MSSA);

    return PreservedAnalyses::all();
  }
};

extern"C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "MemorySSADemoPass", "v0.9",
          [](PassBuilder &PB) {
            PB.registerAnalysisRegistrationCallback(
                [](FunctionAnalysisManager &FAM) {
                  FAM.registerPass([] { return MemorySSAAnalysis(); });
                });

            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "memssa-demo") {
                    FPM.addPass(MemorySSADemoPass());
                    return true;
                  }
                  return false;
                });
          }};
}

