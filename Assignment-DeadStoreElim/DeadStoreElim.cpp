#include "llvm/Analysis/AliasAnalysis.h"
#include "llvm/IR/PassManager.h"
#include "llvm/IR/Function.h"
#include "llvm/Analysis/MemorySSA.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/IR/Instructions.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

struct DeadStoreElimPass : PassInfoMixin<DeadStoreElimPass> {
    PreservedAnalyses run(Function &F, FunctionAnalysisManager &AM){
        auto &MSSAResult = AM.getResult<MemorySSAAnalysis>(F);
        MemorySSA &MSSA = MSSAResult.getMSSA();

        SmallVector<Instruction*, 16> DeadStores; // a list keeping track of deadstores

        // iterating over all basic blocks in reverse order
        for (auto &BB: F){
            for(auto &I : llvm::reverse(BB)){
                auto *MA = MSSA.getMemoryAccess(&I);
                if (!MA){
                    continue;
                }

                auto *MD = dyn_cast<MemoryDef>(MA);
                if (!MD){
                    continue;
                }

                // only considering store instructions now
                auto *Store = dyn_cast<StoreInst>(&I);
                if (!Store){
                    continue;
                }
                // Step 1: find the previous clobber the store overwrote
                MemoryAccess *Prev = MSSA.getWalker()->getClobberingMemoryAccess(MD);
                if(!Prev) continue;

                auto *PrevMD = dyn_cast<MemoryDef>(Prev);
                if(!PrevMD) continue;

                // Step 2: If that clobber is a store to the same location...
                auto *PrevInst = PrevMD->getMemoryInst();
                auto *PrevStore = dyn_cast_or_null<StoreInst>(PrevInst);
                if(!PrevStore) continue;

                auto &AA = AM.getResult<AAManager>(F);
                if (!AA.isMustAlias(Store->getPointerOperand(), PrevStore->getPointerOperand()))
                    continue;
                
                bool InterveningUse = false;
                bool reachedPrev = false;

                for (auto &BB2 : F) {
                    for (auto &I2 : BB2) {
                        auto *MA2 = MSSA.getMemoryAccess(&I2);

                            if (MA2 == PrevMD)
                                reachedPrev = true;
                            if (!reachedPrev)
                                continue;

                            if (MA2 == MD)
                                break;  // stop scanning at current store
                            
                            if (!MA2){
                                continue;
                            }
                            if (isa<MemoryUse>(MA2)) {
                                InterveningUse = true;
                                break;
                            }
                    }
                    if (InterveningUse) break;
                }

                if (!InterveningUse){
                    errs() << "Dead store detected: " << *PrevStore << "\n";
                    DeadStores.push_back(PrevStore);
                }
            }
        }
        // erase dead instructions
        for (auto *I : DeadStores)
            I->eraseFromParent();

        return PreservedAnalyses::all();
    }
};

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "DeadStoreElimPass", "v0.9",
          [](PassBuilder &PB) {
            PB.registerAnalysisRegistrationCallback(
                [](FunctionAnalysisManager &FAM) {
                  FAM.registerPass([] { return MemorySSAAnalysis(); });
                });

            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "dead-store-elim") {
                    FPM.addPass(DeadStoreElimPass());
                    return true;
                  }
                  return false;
                });
          }};
}