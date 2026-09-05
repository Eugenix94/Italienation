import { create } from 'zustand';

export const usePolicyStore = create((set) => ({
  corporateTax: 24.0,
  pensionAge: 67,
  bureaucracyDelay: 100,
  educationInvestment: 4.0,
  
  updateParam: (key, value) => {
    const parsed = parseFloat(value);
    if (!isNaN(parsed)) set((state) => ({ ...state, [key]: parsed }));
  },
  
  resetPolicy: () => set({
    corporateTax: 24.0,
    pensionAge: 67,
    bureaucracyDelay: 100,
    educationInvestment: 4.0,
  })
}));
