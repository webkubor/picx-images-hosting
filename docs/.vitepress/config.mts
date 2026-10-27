import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'free-imgbed',
  description: '开箱即用的 GitHub 免费图床：一个仓库就是一台图床',
  head: [['link', { rel: 'icon', type: 'image/svg+xml', href: '/free-imgbed/logo.svg' }]],
  themeConfig: {
    logo: '/free-imgbed/logo.svg',
    siteTitle: 'free-imgbed',
    nav: [
      { text: '指南', link: '/guide/getting-started' },
      { text: '模板', link: '/guide/templates' },
      { text: 'GitHub', link: 'https://github.com/webkubor/free-imgbed' }
    ],
    sidebar: [
      {
        text: '上手',
        items: [
          { text: '快速开始', link: '/guide/getting-started' },
          { text: '图片命名与链接', link: '/guide/naming-and-links' },
          { text: '查看与管理图片', link: '/guide/browsing' }
        ]
      },
      {
        text: '进阶',
        items: [
          { text: '全局 CLI（imgbed）', link: '/guide/cli' },
          { text: '压缩管线与透明度', link: '/guide/compression' },
          { text: '目录约定', link: '/guide/structure' },
          { text: '自定义域名绑定', link: '/guide/custom-domain' },
          { text: '国内 R2 镜像', link: '/guide/r2-mirror' }
        ]
      },
      {
        text: '其他',
        items: [
          { text: 'AI Agent 接入', link: '/guide/ai-agents' },
          { text: 'CI 与红线', link: '/guide/ci' },
          { text: '引用模板', link: '/guide/templates' }
        ]
      }
    ],
    socialLinks: [{ icon: 'github', link: 'https://github.com/webkubor/free-imgbed' }],
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单'
  }
})
