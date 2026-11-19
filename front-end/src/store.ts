import { create } from 'zustand'

export interface UIState {
  openEvaluatorFilters: (string | number)[]
  toggleOpenEvaluatorFilter: (id: string | number, open: boolean) => void
  resetOpenEvaluatorFilters: () => void
}

export const useUIStore = create<UIState>()(set => ({
  openEvaluatorFilters: [],
  toggleOpenEvaluatorFilter: (id: string | number, open: boolean) =>
    set(state => ({
      openEvaluatorFilters: open
        ? [...state.openEvaluatorFilters, id]
        : state.openEvaluatorFilters.filter(item => item !== id)
    })),
  resetOpenEvaluatorFilters: () =>
    set(() => ({
      openEvaluatorFilters: []
    }))
}))
