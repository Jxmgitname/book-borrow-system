import { validUsername, isExternal } from '@/utils/validate.js'

describe('Utils:validate', () => {
  it('validUsername', () => {
    expect(validUsername('admin')).toBe(true)
    expect(validUsername('editor')).toBe(true)
    expect(validUsername('xxxx')).toBe(true)
    expect(validUsername('ab')).toBe(false)
  })
  it('isExternal', () => {
    expect(isExternal('https://github.com/vuejs/vue')).toBe(true)
    expect(isExternal('http://github.com/vuejs/vue')).toBe(true)
    expect(isExternal('github.com/vuejs/vue')).toBe(false)
    expect(isExternal('/dashboard')).toBe(false)
    expect(isExternal('./dashboard')).toBe(false)
    expect(isExternal('dashboard')).toBe(false)
  })
})
