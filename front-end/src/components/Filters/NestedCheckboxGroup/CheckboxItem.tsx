export interface CheckboxItem {
  key: number | string
  label: number | string
  checked?: boolean
  children?: CheckboxItem[]
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  disabled?: boolean
}
