
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/showlog', component: () => import('layouts/EntireDB.vue') },
      { path: '/popular', component: () => import('layouts/DisplayPopular.vue') },
      { path: '/popularcategory', component: () => import('layouts/PopularCategory.vue') }
    ]
  },

  // Always leave this as last one, but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
