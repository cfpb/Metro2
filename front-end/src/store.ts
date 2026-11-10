import { create } from 'zustand'

export interface UIState {
  openEvaluatorFilters: (string | number)[]
  // addOpenFilter: (id: string | number) => void
  // removeOpenFilter: (id: string | number) => void
  toggleOpenEvaluatorFilter: (id: string | number, open: boolean) => void
  resetOpenEvaluatorFilters: () => void
}

export const useUIStore = create<UIState>()((set) => ({
  openEvaluatorFilters: [],
  // addOpenFilter: (id: string | number) => set(
  //   (state) => (
  //     {
  //       openEvaluatorFilters: [...state.openEvaluatorFilters, id]
  //     }
  //   )
  // ),
  // removeOpenFilter: (id: string | number) => set(
  //   (state) => (
  //     {
  //       openEvaluatorFilters: state.openEvaluatorFilters.filter((item) => item !== id)
  //     }
  //   )
  // ),
  toggleOpenEvaluatorFilter: (id: string | number, open: boolean) => set(
    (state) => (
      {
        openEvaluatorFilters: open ?
          [...state.openEvaluatorFilters, id]
          : state.openEvaluatorFilters.filter((item) => item !== id)
      }
    )
  ),
  resetOpenEvaluatorFilters: () => set(
    () => (
      {
        openEvaluatorFilters: []
      }
    )
  ),

}))

