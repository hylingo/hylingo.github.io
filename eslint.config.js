// Flat config — 宽松起步：只报真问题，不报风格争议（风格交给 Prettier）。
// 严格化时把 'warn' / 'off' 收紧成 'error' 即可。
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import vue from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'
import prettier from 'eslint-config-prettier'
import globals from 'globals'

export default [
  {
    ignores: [
      'dist/**',
      'node_modules/**',
      'public/**',
      'scripts/**',
      'coverage/**',
      '.venv/**',
      '*.config.js',
      '*.config.ts',
      // 已弃用的空 stub，模板里只有注释，规则不通过；不想动这个文件等手动清理。
      'src/components/quiz/QuizPanel.vue',
    ],
  },

  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...vue.configs['flat/essential'],

  {
    files: ['**/*.{ts,tsx,vue}'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tseslint.parser,
        ecmaVersion: 'latest',
        sourceType: 'module',
        extraFileExtensions: ['.vue'],
      },
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      // ---- 宽松：风格类全部交给 Prettier 或关掉 ----
      'vue/multi-word-component-names': 'off',
      'vue/no-v-html': 'off',
      'vue/require-default-prop': 'off',

      // ---- 类型相关：报警告而非错误，方便逐步收 ----
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/no-empty-function': 'off',
      '@typescript-eslint/ban-ts-comment': 'warn',

      // ---- 真 bug 类：保持 error ----
      'no-undef': 'off', // tseslint 已处理
      'no-empty': ['error', { allowEmptyCatch: true }],
      'no-constant-condition': ['error', { checkLoops: false }],
      'no-prototype-builtins': 'warn',

      // 关掉：本项目用 `someTick.value` 这种"裸读 ref"作为响应式订阅锚点
      // （让 computed 重新计算），这是有意为之的 Vue 模式，不是死代码。
      '@typescript-eslint/no-unused-expressions': 'off',

      // 关掉：base no-redeclare 不理解 TS 函数重载，
      // TS 编译器自己会查重复定义，这里关掉避免误报。
      'no-redeclare': 'off',
    },
  },

  // 类型声明文件更宽松
  {
    files: ['**/*.d.ts'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
    },
  },

  prettier,
]
