export interface CheckboxItem {
  key: number | string
  name: number | string
  checked?: boolean
  children?: CheckboxItem[]
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}
