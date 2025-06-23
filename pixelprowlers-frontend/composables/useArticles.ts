export interface Article {
  slug: string
  title: string
  date: string
  category: string
  cover: string
  content: string
}

const articleMock: Record<string, Article> = {
  'premier-article': {
    slug: 'premier-article',
    title: 'Premier article mocké',
    date: '2024-06-01',
    category: 'Tech',
    cover: '/paysage-depart.jpg',
    content: `
      <p>Voici le contenu riche de l\u2019article. Il peut comporter des balises <strong>HTML</strong> vari\u00e9es.</p>
      <blockquote>La connaissance est une lumi\u00e8re qui r\u00e9chauffe l\u2019\u00e2me.</blockquote>
      <p>Chaque paragraphe transporte le lecteur vers un nouvel horizon.</p>
    `,
  },
}

export async function useArticle(slug: string): Promise<Article> {
  return Promise.resolve(articleMock[slug] || articleMock['premier-article'])
}