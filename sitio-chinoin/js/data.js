/*
 * Contenido del sitio. La estructura (menús, secciones, categorías y textos del
 * Portal Médico) es la de chinoin.com/es tal como aparece en las capturas.
 *
 * Los campos marcados con PENDIENTE no se pudieron leer de chinoin.com desde este
 * entorno (el dominio está bloqueado por la red de la sesión). Se dejan vacíos o con
 * texto neutro para que se reemplacen por el contenido original, sin inventarlo.
 */
window.CHINOIN = {
  nav: [
    {
      label: 'Nosotros', key: 'nosotros',
      items: [
        { label: 'Calidad', route: '#/nosotros/calidad' },
        { label: 'Responsabilidad Social', route: '#/nosotros/responsabilidad-social' },
        { label: 'Tecnología', route: '#/nosotros/tecnologia' }
      ]
    },
    { label: 'Productos', key: 'productos', mega: true },
    {
      label: 'Unidades de Negocio', key: 'unidades',
      items: [
        { label: 'Mercado privado', route: '#/unidades/mercado-privado' },
        { label: 'Venta a gobierno', route: '#/unidades/venta-a-gobierno' },
        { label: 'Exportaciones', route: '#/unidades/exportaciones' },
        { label: 'Maquilas', route: '#/unidades/maquilas' },
        { label: 'Huéspedes', route: '#/unidades/huespedes' }
      ]
    },
    {
      label: 'Contacto', key: 'contacto',
      items: [
        { label: 'Únete al equipo', route: '#/contacto/unete-al-equipo' },
        { label: 'Farmacovigilancia', route: '#/contacto/farmacovigilancia' }
      ]
    },
    { label: 'Portal Médico', key: 'portal', href: 'portal-medico.html' }
  ],

  // Grupos del mega menú de Productos, en el mismo orden que el sitio original.
  productGroups: [
    {
      key: 'areas-terapeuticas', label: 'Áreas Terapéuticas', icon: 'file',
      categories: [
        'Respiratorio', 'Gastrointestinales', 'Ginecológicos',
        'Cardiovasculares', 'Músculo-esqueléticos', 'Corticoesteroides'
      ]
    },
    {
      key: 'cuidado-de-la-salud', label: 'Cuidado de la salud', icon: 'house',
      categories: [
        'Gripe y resfriado', 'Tos', 'Piojos', 'Acidez estomacal',
        'Diarrea', 'Estreñimiento', 'Sarna', 'Fiebre y dolor'
      ]
    },
    { key: 'benebioticos', label: 'Benebióticos', icon: 'apple', categories: [] },
    { key: 'odontologia', label: 'Odontología', icon: 'teeth', categories: [] },
    { key: 'veterinaria', label: 'Veterinaria', icon: 'paw', categories: [] }
  ],

  /*
   * PENDIENTE: catálogo de productos de chinoin.com.
   * Formato de cada producto:
   * {
   *   id: 'nombre-del-producto',
   *   name: 'Nombre®',
   *   category: 'gripe-y-resfriado',      // slug de la categoría o del grupo
   *   image: 'assets/productos/archivo.png',
   *   summary: 'Texto original de la ficha',
   *   buyUrl: 'https://…'                  // enlace de compra que usa el sitio original
   * }
   */
  products: [],

  // PENDIENTE: textos originales de cada página interna.
  pages: {
    nosotros: {
      calidad: { title: 'Calidad', kicker: 'Nosotros', body: [] },
      'responsabilidad-social': { title: 'Responsabilidad Social', kicker: 'Nosotros', body: [] },
      tecnologia: { title: 'Tecnología', kicker: 'Nosotros', body: [] }
    },
    unidades: {
      'mercado-privado': { title: 'Mercado privado', kicker: 'Unidades de Negocio', body: [] },
      'venta-a-gobierno': { title: 'Venta a gobierno', kicker: 'Unidades de Negocio', body: [] },
      exportaciones: { title: 'Exportaciones', kicker: 'Unidades de Negocio', body: [] },
      maquilas: { title: 'Maquilas', kicker: 'Unidades de Negocio', body: [] },
      huespedes: { title: 'Huéspedes', kicker: 'Unidades de Negocio', body: [] }
    },
    contacto: {
      'unete-al-equipo': { title: 'Únete al equipo', kicker: 'Contacto', body: [] },
      farmacovigilancia: { title: 'Farmacovigilancia', kicker: 'Contacto', body: [] }
    }
  }
};
