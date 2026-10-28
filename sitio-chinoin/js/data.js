/*
 * Contenido del sitio, copiado tal cual de chinoin.com/es (octubre 2026).
 * Las rutas (#/…) usan las mismas direcciones que el sitio original para que sea fácil comparar.
 * El catálogo de productos está en js/catalogo.js y las fichas en js/fichas.js (generados con tools/).
 */
window.CHINOIN = {
  links: {
    portalMedico: 'https://emc.chinoin.com/',
    veterinaria: 'https://www.chinoinveterinaria.com/sitio/',
    original: 'https://www.chinoin.com/es/',
    social: [
      { label: 'LinkedIn', href: 'https://www.linkedin.com/company/chinoinpf/', icon: 'linkedin' },
      { label: 'X', href: 'https://x.com/chinoinpf', icon: 'x' },
      { label: 'YouTube', href: 'https://youtube.com/@chinoinpf', icon: 'youtube' }
    ]
  },

  // Menú principal, en el mismo orden y con las mismas etiquetas que el original.
  nav: [
    {
      label: 'Nosotros', key: 'nosotros',
      items: [
        { label: 'Calidad', route: '#/calidad-chinoin' },
        { label: 'Responsabilidad Social', route: '#/responsabilidad-social' },
        { label: 'Tecnología', route: '#/tecnologia' }
      ]
    },
    { label: 'Productos', key: 'productos', route: '#/catalogo', mega: true },
    {
      label: 'Unidades de Negocio', key: 'unidades', route: '#/unidades-de-negocio',
      items: [
        { label: 'Mercado privado', route: '#/unidades-de-negocio/mercado-privado' },
        { label: 'Venta a gobierno', route: '#/unidades-de-negocio/venta-a-gobierno' },
        { label: 'Exportaciones', route: '#/unidades-de-negocio/exportaciones' },
        { label: 'Maquilas', route: '#/unidades-de-negocio/maquilas' },
        { label: 'Huéspedes', route: '#/unidades-de-negocio/huespedes' }
      ]
    },
    {
      label: 'Contacto', key: 'contacto', route: '#/contacto',
      items: [
        { label: 'Únete al equipo', route: '#/unete-al-equipo' },
        { label: 'Farmacovigilancia', route: '#/farmacovigilancia' }
      ]
    },
    { label: 'Portal Médico', key: 'portal', href: 'portal-medico.html' }
  ],

  // Mega menú de Productos (mismo orden que el original)
  megaGroups: [
    {
      label: 'Áreas Terapéuticas', icon: 'file', route: '#/medicamentos-prescripcion',
      items: [
        { label: 'Respiratorio', route: '#/portafolio-respiratorios' },
        { label: 'Gastrointestinales', route: '#/portafolio-gastrointestinales' },
        { label: 'Ginecológicos', route: '#/portafolio-ginecologicos' },
        { label: 'Cardiovasculares', route: '#/portafolio-cardiovasculares' },
        { label: 'Músculo-esqueléticos', route: '#/portafolio-musculo-esqueleticos' },
        { label: 'Corticoesteroides', route: '#/portafolio-corticoesteroides' }
      ]
    },
    { label: 'Benebióticos', icon: 'apple', route: '#/probioticos', items: [] },
    { label: 'Odontología', icon: 'teeth', route: '#/odontologia', items: [] },
    { label: 'Veterinaria', icon: 'paw', route: '#/veterinaria', items: [] },
    {
      label: 'Cuidado de la salud', icon: 'house', route: '#/cuidado-de-la-salud',
      items: [
        { label: 'Gripe y resfriado', route: '#/gripe-y-resfriado' },
        { label: 'Tos', route: '#/tos' },
        { label: 'Piojos', route: '#/piojos' },
        { label: 'Acidez estomacal', route: '#/acidez-estomacal' },
        { label: 'Diarrea', route: '#/diarrea' },
        { label: 'Estreñimiento', route: '#/estrenimiento' },
        { label: 'Sarna', route: '#/sarna' },
        { label: 'Fiebre y dolor', route: '#/fiebre-y-dolor' }
      ]
    }
  ],
  megaPromo: { text: 'Cumplimos 100 años de atención a la salud de los mexicanos.', img: 'assets/img/logo-100-chinoin.webp', route: '#/libro-100' },

  home: {
    banners: [
      { img: 'assets/img/banner-greatplace-chinoin.webp', alt: 'banner-greatPlace-chinoin' },
      { img: 'assets/img/banner-conexion-chinoin.webp', alt: 'banner-conexion-chinoin' },
      { img: 'assets/img/banner-100-anos.webp', alt: 'Banner-100-años', route: '#/libro-100' }
    ],
    h1: 'Farmacéutica Mexicana',
    intro: 'Somos una empresa orgullosamente mexicana con 100 años de historia, eficacia, confianza y plenitud para tu familia.',
    preguntas: [
      { q: '¿Qué hacemos?', a: 'Brindamos soluciones terapéuticas con precio justo.' },
      { q: '¿Para qué lo hacemos?', a: 'Para ofrecer soluciones que mejoren la calidad de vida de la sociedad.' },
      { q: '¿Cómo lo hacemos?', a: 'Siendo socialmente responsables con productos líderes en el mercado, a través de la tecnología con altos estándares de calidad, todo esto a través de nuestra gente.' }
    ],
    experienciaImg: 'assets/img/chinoin-experiencia-266x280.webp',
    pilares: {
      title: 'Nuestros pilares',
      p: [
        'A través de nuestros 5 pilares buscamos tener congruencia con lo que hacemos.',
        'Siendo una empresa dedicada al bienestar de cada uno de sus colaboradores y de la sociedad lo que hoy en día nos ha apoyado en nuestro crecimiento a lo largo de los años.'
      ],
      // Los 5 pilares, como aparecen en el círculo de la imagen original
      items: [
        { label: 'Gente' },
        { label: 'Productos', route: '#/catalogo' },
        { label: 'Calidad', route: '#/calidad-chinoin' },
        { label: 'Tecnología', route: '#/tecnologia' },
        { label: 'Responsabilidad Social', route: '#/responsabilidad-social' }
      ]
    },
    presencia: {
      title: 'Presencia',
      p: [
        'Actualmente contamos con 3 plantas ubicadas en: Ciudad de México, Aguascalientes y Colombia.',
        'Además contamos con presencia comercial en México, así como 8 países en Centro y Sudamérica, siempre buscando expandirnos a más países.'
      ],
      img: 'assets/img/chinoin-en-america.webp'
    },
    historia: { title: 'Nuestra historia', img: 'assets/img/infografia-timeline.webp' },
    // Línea del tiempo transcrita de la infografía original (infografia-timeline.png).
    // <b> = énfasis morado, <em> = énfasis naranja, como en la infografía.
    timeline: [
      { y: 1912, img: 'assets/img/historia/hex-1912.webp', t: 'Todo inicia en el año 1912 cuando Chinoin <b>fue fundada en Hungría</b> como fábrica de productos farmacéuticos.' },
      { y: 1925, img: 'assets/img/historia/hex-1925.webp', t: 'Inicia sus <b>operaciones en México</b> como <em>Chinoin</em> fabrica de productos <em>Químicos y Farmacéuticos</em> con productos terminados de <b>Hungría.</b>' },
      { y: 1932, img: 'assets/img/historia/hex-1932.webp', t: 'Se constituye <b>Productos Farmacéuticos S. A. de C.V.</b> Hoy conocida como <em>Chinoin</em> empresa <b>100% Mexicana</b> e inicia la fabricación nacional de medicamentos en la planta <em>Ciudad de México.</em>' },
      { y: 1942, img: 'assets/img/historia/hex-1942.webp', t: '<em>CHINOIN</em> a consecuencia de la <b>segunda guerra mundial</b> se separa de la matriz en <b>Hungría,</b> <em>comenzando el desarrollo de formulas propias</em> e iniciando la exportación a países de Centroamérica.' },
      { y: 1950, img: 'assets/img/historia/hex-1950.webp', t: 'Se cuenta ya con <em>17 productos</em> principalmente: <b>analgésicos, antitusígenos y antiinfecciosos.</b>' },
      { y: 1960, img: 'assets/img/historia/hex-1960.webp', t: '<em>CHINOIN</em> inicia el desarrolllo y comercialización de <b>productos para el mercado de</b> <em>Salud Animal</em>.' },
      { y: 1971, img: 'assets/img/historia/hex-1971.webp', t: '<em>CHINOIN</em> hace convenio con <b>Janssen Pharma</b> para importar y distribuir productos veterinarios en México.' },
      { y: 1987, img: 'assets/img/historia/hex-1987.webp', t: 'Se construye la <b>planta farmoquímica</b> en el estado de <em>Aguascalientes.</em>' },
      { y: 1988, img: 'assets/img/historia/hex-1988.webp', t: 'Cambia la estrategia comercial. La nueva fuerza de ventas fue integrada por personas con <b>20 años de experiencia</b> mínimo en el ramo farmacéutico, convirtiéndose en la fuerza de ventas <b>más productiva de la industria.</b>' },
      { y: 2000, img: 'assets/img/historia/hex-2000.webp', t: 'Se inaugura la planta en <b>Aguacalientes</b> iniciando operaciones con el <em>área sólidos y líquidos orales.</em>' },
      { y: 2004, img: 'assets/img/historia/hex-2004.webp', t: 'Comienza la construcción de la <em>segunda fase de la planta farmacéutica en Aguascalientes</em> teniendo expansión en inyectables, cremas y líquidos tópicos, desarrollo Galénico, desarrollo Analítico, así como las oficinas administrativas.<br><br>La <b>PROFEPA</b> nos certifica como <em>industria Limpia</em>' },
      { y: 2010, img: 'assets/img/historia/hex-2010.webp', t: 'Remodelación de oficinas planta México e inauguración del <b>nuevo corporativo en Ciudad de México.</b>' },
      { y: 2014, img: 'assets/img/historia/hex-2014.webp', t: 'Se construye el <em>Almacén Robotizado de alta</em> estiba con <b>tecnología de Stöcklin.</b>' },
      { y: 2015, img: 'assets/img/historia/hex-2015.webp', t: 'Inicia operaciones el equipo <em>CONSIGMA,</em> proviene del termino proceso continuo “con” mientras que sigma hace referencia a la metodología <em>6-SIGMA</em>, empleada en la mejora de procesos, es un sistema cerrado de granulación continua con capacidades de 500 gramos hasta toneladas, <em>único en América latina.</em><br><br>Entra en función la <b>planta de trigeneración de energía</b> cuyo proceso consiste en la <b>autogeneración de energía: eléctrica, vapor industrial y agua helada</b> a partir de la combustión de gas natural en nuestra planta de Aguascalientes.' },
      { y: 2017, img: 'assets/img/historia/hex-2017.webp', t: 'Se inaugura un nuevo <em>Laboratorio microbiólogico</em> para ampliar nuestras operaciones de calidad. Se establecen los nuevos valores y cultura de la compañía, así como nuestro slogan <b>“Experiencia que da vida”.</b>' },
      { y: 2018, img: 'assets/img/historia/hex-2018.webp', t: 'Se adquiere <b>Farmacol</b> en Colombia naciendo <em>Chinoin Farmacol</em> es ese país.' },
      { y: 2019, img: 'assets/img/historia/hex-2019.webp', t: '<em>Chinoin</em> es <em>reconocida</em> como <b>empresa socialmente responsable.</b>' },
      { y: 2020, img: 'assets/img/historia/hex-2020.webp', t: 'La PROFEPA nos otorga el certificado de industria limpia Nivel 2 por el cumplimiento <b>legal y normativo, así como demostrar mejoras</b> en agua, residuos peligrosos, no peligrosos y de manejo especial, emisiones a la atmósfera, suelo, ruido, riesgo ambiental, <em>aprovechamiento de los recursos naturales y sistemas de gestión ambiental.</em>' },
      { y: 2024, img: 'assets/img/historia/hex-2024.webp', t: 'AntifluDes <b>cumple 50 años</b> siendo el principal antigripal de triple acción.' },
      { y: 2025, img: 'assets/img/historia/hex-2025.webp', t: 'Chinoin® <em>cumple 100 años</em> de atención a la salud de los mexicanos.' }
    ],
    // Banners de la portada original, recreados con texto real (mismos textos y fotos, en alta resolución)
    slides: [
      {
        id: 'gptw', route: '#/unete-al-equipo',
        badge: 'assets/img/hq/gptw-badge.webp', badgeAlt: 'Los Mejores Lugares para Trabajar · Great Place To Work · México 2026',
        photo: 'assets/img/hq/planta-aerea.webp',
        title: 'Las personas están en el centro de todo lo que hacemos.'
      },
      {
        id: 'conexion', href: 'portal-medico.html',
        logo: 'assets/img/hq/conexion-logo.webp',
        photo: 'assets/img/hq/conexion-medicos.webp',
        title: 'Toda la <b>información médica</b> especializada que necesita, de forma rápida, práctica a <em>un clic de distancia.</em>',
        tag: 'Conectando con lo <em>que importa</em>'
      },
      {
        id: 'cien', route: '#/libro-100',
        photo: 'assets/img/hq/cien-gente.webp', bg: 'assets/img/chinoin-4.webp',
        big: '100 años',
        title: 'De historias, retos y aprendizajes que nos han definido.',
        band: 'Pero, sobre todo, nuestra gente',
        tag: 'El corazón de esta historia'
      }
    ],
    circulo: {
      title: 'El círculo dorado Chinoin®',
      img: 'assets/img/circulo-dorado-chinoin-374x340.webp',
      p: [
        'Nuestra razón de ser “Ofrecer soluciones que mejoren la calidad de vida de la sociedad”. ha sido la guía para formar lo que hoy conocemos como “El Círculo Dorado de Chinoin®”, el cual esta integrado por nuestros 5 pilares que son el reflejo de los principios y valores que vivimos como empresa.',
        'El Círculo Dorado de Chinoin® forma parte de nuestra cultura y ADN, lo que nos impulsa día a día a brindar soluciones terapéuticas con precio justo para cada uno de nuestros clientes de las diferentes líneas humana y veterinaria con las que contamos.'
      ]
    }
  },

  calidad: {
    title: 'Le damos gran valor a la Calidad',
    header: 'assets/img/header-calidad-website.webp',
    lead: 'Además del reconocimiento a la calidad, eficacia y seguridad de los productos CHINOIN®',
    p: 'por parte de la comunidad médica y del público usuario, nuestras instalaciones ostentan diversas certificaciones que acreditan no sólo esta calidad, sino también las buenas prácticas de fabricación de medicamentos y la excelencia que nos caracterizan en cada uno de los procesos.',
    img: { src: 'assets/img/inside-image-calidad.webp', caption: 'Innovación en medicamentos.' },
    cert: {
      img: 'assets/img/industria-limpia.webp',
      html: 'Entre estas certificaciones, contamos con la de <strong>Industria Limpia</strong>, emitida por PROFEPA, la cual avala nuestro compromiso con el cuidado del medio ambiente y la protección de la ecología.'
    }
  },

  responsabilidad: {
    title: 'Le damos gran valor a la Responsabilidad Social',
    header: 'assets/img/header-responsabilidad-social-website.webp',
    intro: 'En Chinoin sabemos la importancia de la responsabilidad social, por eso nos preocupamos por preservar un mundo mejor, promoviendo diferentes acciones a través de 3 ejes:',
    ejes: [
      { label: 'Medio ambiente', img: 'assets/img/responsabilidad-social-chinoin-1-3.webp' },
      { label: 'Cultura interna hacia colaboradores', img: 'assets/img/responsabilidad-social-chinoin-1-6.webp' },
      { label: 'Comunidad', img: 'assets/img/responsabilidad-social-chinoin-1-2.webp' }
    ],
    programa: {
      title: 'Programa Neutralízate',
      p: [
        'Conscientes de la responsabilidad social que tenemos como empresa, nos hemos convertido no sólo en una Industria Limpia, sino también en una Empresa Neutra.',
        'Para ello, nos sumamos a diversos programas encaminados a promover la protección de la ecología, así como mejorar la calidad de vida de las personas, como por ejemplo:'
      ],
      items: [
        {
          title: 'Industria Limpia', img: 'assets/img/industria-limpia-2-1.webp',
          p: ['El “Programa Neutralízate”, cuyo objetivo es disminuir y mitigar las emisiones de Gases de Efecto Invernadero «GEI” como un instrumento que ayude a reducir el cambio climático, conservar los ecosistemas y ayudar a las comunidades rurales a tener alternativas sustentables de desarrollo.']
        },
        {
          title: 'Empresa Socialmente Responsable', img: 'assets/img/empresa-socialmente-responsable-chinoin.webp',
          p: [
            'Adicional, la planta de Aguascalientes cuenta con el Distintivo ESR como resultado del compromiso público y voluntario de implementar una gestión socialmente responsable.',
            'Este distintivo es el reflejo de la buena implementación que se ha realizado gracias los 3 ejes de acción de Responsabilidad Social.'
          ]
        }
      ]
    }
  },

  tecnologia: {
    title: 'Le damos un gran valor a la Tecnología',
    header: 'assets/img/header-tecnologia-website.webp',
    instalaciones: {
      title: 'Instalaciones',
      p: [
        'Dentro de nuestras plantas, contamos con áreas de producción de sólidos, líquidos e inyectables.',
        'Equipadas con tecnología de punta y los procesos más avanzados en automatización, entre los cuales destaca nuestro almacén totalmente automatizado, ya que no cuenta con operador a bordo.'
      ],
      items: ['Contención de Producto', 'Tranferencia de Gravedad', 'Almacenaje', 'Limpieza y esterilización en Sitio', 'Mezclado en contenedores'],
      // Fotos de alta resolución (Unsplash) en lugar de las originales de 390×260 px; el almacén es foto original.
      gallery: [
        { src: 'assets/img/almacen-chinoin-video.webp', alt: 'almacen-chinoin-video', video: 'https://www.youtube.com/watch?v=J_RZoEkLuq4&t=11s' },
        { src: 'assets/img/stock/lab-corredor.webp', alt: 'Laboratorio de control de calidad' },
        { src: 'assets/img/stock/lab-equipo.webp', alt: 'Equipo de laboratorio' },
        { src: 'assets/img/stock/lab-viales.webp', alt: 'Inyectables' },
        { src: 'assets/img/stock/lab-pipeta.webp', alt: 'Análisis de laboratorio' },
        { src: 'assets/img/stock/blisters-2.webp', alt: 'Tabletas y cápsulas' },
        { src: 'assets/img/stock/lab-mujer.webp', alt: 'Laboratorio' }
      ]
    },
    equipamiento: {
      title: 'Equipamiento',
      p: 'Contamos con equipo avanzado como:',
      items: ['Bins de mezclado', 'Encapsuladoras', 'Llenadoras de polvos', 'Emblistadoras, estuchadoras y Etiquetadoras', 'Esterilización en sitio CIP/SIP', 'Tren de llenado (ampolleta y frasco vial)', 'Tableteadoras']
    },
    innovacion: {
      title: 'Innovación',
      items: [
        { img: 'assets/img/tecnologia-chinoin-2.webp', html: 'CHINOIN® tiene autosuficiencia eléctrica gracias a la planta de trigeneración que produce electricidad, vapor de agua y chiller para aire acondicionado.' },
        { img: 'assets/img/tecnologia-chinoin-4-1.webp', html: 'Se producen <strong>1,700 megawatts-hora</strong> al mes en la planta de Aguascalientes.' },
        { img: 'assets/img/tecnologia-chinoin-2-1.webp', html: 'Con una inversión de <strong>5.7 millones de dólares</strong>, vende los kilowatts excedentes a la CFE (Comisión Federal de Electricidad), aprovechando al máximo la Reforma energética.' },
        { img: 'assets/img/tecnologia-chinoin-1.webp', html: 'Al utilizar el gas natural como fuente de energía, se redujo la huella de carbono en un <strong>80%</strong>, lo que motiva a participar en la primera subasta eléctrica en el país.' },
        { img: 'assets/img/tecnologia-chinoin-4-2.webp', html: 'Dicha subasta tendrá 3 modalidades:', list: ['Generación a corto plazo', 'Potencia', 'Certificado de energía limpia'] }
      ],
      closing: 'Sin duda en CHINOIN® somos una empresa que crece y se moderniza día a día.'
    }
  },

  unidades: {
    title: 'Unidades de Negocio',
    header: 'assets/img/header-unidades-negocio-website.webp',
    items: [
      {
        id: 'mercado-privado', title: 'Mercado Privado', img: 'assets/img/fabricacion-de-medicamentos.webp',
        p: ['Enfocado a comercialización, fabricación y desarrollo de medicamentos para la salud humana en el territorio mexicano y participación en importantes segmentos dentro de los que destacan productos para terapia:'],
        list: ['Respiratoria', 'Musculo-esquelética', 'Gastrointestinal']
      },
      {
        id: 'venta-a-gobierno', title: 'Venta a gobierno', img: 'assets/img/proveedor-medicamentos-gobierno-chinoin.webp',
        p: ['Gracias a la reconocida calidad de nuestros productos y a los más de 100 años de experiencia que nos respaldan, nos convertimos en proveedores permanentes de medicamentos para el Sistema Nacional de Salud en México.']
      },
      {
        id: 'exportaciones', title: 'Exportaciones', img: 'assets/img/exportaciones-website-4.webp', wide: true,
        lead: 'Exportamos productos a Centroamérica, parte de Sudamérica y el Caribe.',
        p: ['Uno de nuestros objetivos de crecimiento y expansión es llegar a ser una empresa mexicana con presencia dentro del mercado farmacéutico latinoamericano.']
      },
      {
        id: 'maquilas', title: 'Maquilas', img: 'assets/img/maquila-medicamentos-chinoin.webp',
        p: ['Contamos con la capacidad, instalaciones y tecnología avanzada para la fabricación de productos, tanto para uso humano como veterinario, en diversas presentaciones o formas farmacéuticas:'],
        list: ['Tabletas', 'Cápsulas', 'Cremas y ungüentos', 'Jarabes y suspensiones', 'Polvos para preparar suspensiones orales', 'Supositorios', 'Suspensiones inyectables', 'Soluciones inyectables', 'Soluciones nasales', 'Soluciones oftálmicas']
      },
      {
        id: 'huespedes', title: 'Huéspedes', img: 'assets/img/proveedor-medicamentos-gobierno-chinoin-1.webp',
        p: ['Apoyados en nuestra experiencia, infraestructura, tecnología, calidad y personal calificado, ofrecemos a la industria farmacéutica un servicio integral especializado que incluye:'],
        list: ['Mantenimiento de registros, permisos de importación.', 'Apoyo y seguimiento de trámites antes COFEPRIS.', 'Fabricación, acondicionado, almacenaje y distribución de productos.']
      }
    ]
  },

  contacto: {
    title: 'Contáctanos',
    header: 'assets/img/header-contacto-website.webp',
    sedes: [
      {
        title: 'Oficinas generales y planta en México',
        lines: ['Lago Tangañica #18, Colonia Granada, 11520 México,D.F.'],
        tel: [{ label: 'Teléfono', value: '(52) (55) 5262 31 00', href: 'tel:+525552623100' }, { label: 'Fax', value: '(52) (55) 5531 43 49' }]
      },
      {
        title: 'Planta en Aguascalientes',
        lines: ['Carretera Pabellón de Hidalgo km. 4.2 Municipio Rincón de', 'Romos, 20420 Aguascalientes'],
        tel: [{ label: 'Teléfono y fax', value: '(52)(465) 9581804', href: 'tel:+524659581804' }]
      }
    ],
    directorioTitle: 'Directorio de email',
    directorio: [
      ['Ventas', 'ventas@chinoin.com'],
      ['Ventas Exportación', 'vexport@chinoin.com'],
      ['Compras', 'compras@chinoin.com'],
      ['Contacto huéspedes', 'huespedes@chinoin.com'],
      ['Credito y Cobranza', 'credito@chinoin.com'],
      ['Dirección Médica', 'dirmed@chinoin.com'],
      ['Farmacovigilancia', 'farmacovigilancia@chinoin.com'],
      ['Maquilas', 'maquilas@chinoin.com'],
      ['Pagos', 'pagos@chinoin.com'],
      ['Recursos Humanos Ciudad de México', 'recepcvmex@chinoin.com'],
      ['Recursos Humanos Aguascalientes', 'recepcvags@chinoin.com'],
      ['Tecnologías de Información', 'ti@chinoin.com']
    ]
  },

  farmacovigilancia: {
    title: 'Farmacovigilancia',
    header: 'assets/img/header-farmacovigilancia-website.webp',
    intro: 'Si usted ha presentado una sospecha de reacción adversa (malestar) asociado al uso de algún medicamento de Productos Farmacéuticos, S.A de C.V., agradeceremos notificar su reporte a la Unidad de Farmacovigilancia a través de las siguientes vías:',
    vias: [
      { label: 'Teléfono área metropolitana', value: '55 52 62 31 88', href: 'tel:+525552623188' },
      { label: 'LADA sin costo', value: '800 8419 192', href: 'tel:8008419192' },
      { label: 'Correo electrónico', value: 'farmacovigilancia@chinoin.com', href: 'mailto:farmacovigilancia@chinoin.com' }
    ],
    formTitle: 'Formulario en línea',
    // Mismo formulario de HubSpot que usa el sitio original (campos tal cual)
    hubspot: { portalId: '48099646', formId: '2602e084-a47d-4b92-9993-4e6906333b5e' },
    form: {
      submit: 'Enviar',
      gracias: 'Gracias por enviar el formulario.',
      groups: [
        {
          title: 'Información de la persona que presenta el reporte:',
          fields: [
            { name: 'firstname', label: 'Nombre', type: 'text', req: true },
            { name: 'lastname', label: 'Apellidos', type: 'text', req: true },
            { name: 'phone', label: 'Número de teléfono', type: 'tel' },
            { name: 'email', label: 'Correo', type: 'email', req: true }
          ]
        },
        {
          title: 'Información del paciente',
          fields: [
            { name: 'iniciales', label: 'Iniciales', type: 'text', req: true },
            { name: 'genero', label: 'Genero', type: 'select', options: ['Hombre', 'Mujer'], req: true }
          ]
        },
        {
          title: 'Nombre del medicamento',
          fields: [
            { name: 'datos_del_medicamento', label: 'Nombre del medicamento', type: 'textarea', req: true },
            { name: 'presentacion', label: 'Presentación', type: 'textarea', req: true },
            { name: 'lote', label: 'Lote', type: 'text' },
            { name: 'indicacion', label: 'Indicación', type: 'textarea' },
            { name: 'dosis', label: 'Dosis', type: 'textarea' },
            { name: 'fecha_de_inicio_del_tratamiento', label: 'Fecha de inicio del tratamiento', type: 'date' },
            { name: 'descripcion_de_la_sospecha_de_reaccion_adversa', label: 'Descripción de la reacción adversa sospechada (malestar)', type: 'textarea', req: true, full: true },
            { name: 'fecha_de_inicio_de_la_sospecha_de_reaccion_adversa__malestar_', label: 'Fecha de inicio de la sospecha de reacción adversa (malestar)', type: 'date' },
            { name: 'se_suspendio_el_tratamiento_', label: '¿Se suspendió el tratamiento?', type: 'select', options: ['Si', 'No'] },
            { name: 'comentarios', label: 'Comentarios', type: 'textarea', full: true }
          ]
        }
      ]
    }
  },

  // PENDIENTE: chinoin.com/es/unete-al-equipo no se pudo leer desde este entorno.
  unete: {
    title: 'Únete al equipo',
    hubspot: { portalId: '48099646', formId: 'aaa90a59-33b0-4b70-a4f8-94b568d90d50' },
    contactos: [
      ['Recursos Humanos Ciudad de México', 'recepcvmex@chinoin.com'],
      ['Recursos Humanos Aguascalientes', 'recepcvags@chinoin.com']
    ]
  },

  biblioteca: {
    title: 'Biblioteca Virtual',
    items: [
      { title: 'Influenza, amenaza latente', img: 'assets/img/influenza-amenaza-latente.webp', pdf: 'https://www.chinoin.com/hubfs/Influenza-Amenaza-Latente-2019_compressed.pdf' },
      { title: 'El reto de ser médico 3.º Edición', img: 'assets/img/el-reto-de-ser-medico.webp', pdf: 'https://www.chinoin.com/hubfs/Libro-el-reto-de-ser-medico.pdf' },
      { title: 'COVID Consentimiento informado menor', img: 'assets/img/covid-consentimiento-menor.webp', pdf: 'https://www.chinoin.com/hubfs/COVID-CONSENTIMIENTO-INFORMADO-MENOR-1.pdf' },
      { title: 'COVID Consentimiento informado 2020', img: 'assets/img/covid-consentimiento-2020.webp', pdf: 'https://www.chinoin.com/hubfs/COVID-CONSENTIMIENTO-INFORMADO-2020.pdf' },
      { title: 'Dexametasona, vigencia y permanencia', img: 'assets/img/dexametasona.webp', pdf: 'https://www.chinoin.com/hubfs/Dexametasona-Vigencia-y-permanencia-Ed_digital-21-julio.pdf' }
    ]
  },

  libro100: {
    banner: 'assets/img/banner-100-anos.webp',
    libro: 'https://online.fliphtml5.com/nnxql/zcek/',
    title: 'Te invitamos a descubrir nuestra historia',
    p: 'Aquí encontrarás los momentos que han definido nuestro camino: los inicios, los desafíos superados, las transformaciones y los logros que nos han llevado a ser quienes somos. Conecta con nuestras raíces y celebremos juntos un legado que sigue creciendo.',
    fotos: ['assets/img/chinoin-1.webp', 'assets/img/chinoin-4.webp', 'assets/img/chinoin-3.webp', 'assets/img/chinoin-5.webp', 'assets/img/chinoin-2.webp']
  },

  prescripcion: {
    kicker: 'Áreas Terapéuticas',
    title: 'Medicamentos de prescripción',
    intro: 'Conoce a detalle toda la información de nuestro portafolio de medicamentos de prescripción médica.',
    cards: [
      { label: 'Respiratorios', img: 'assets/img/medicamentos-respiratorios-chinoin.webp', route: '#/portafolio-respiratorios' },
      { label: 'Gastrointestinales', img: 'assets/img/medicamentos-gastrointestinales.webp', route: '#/portafolio-gastrointestinales' },
      { label: 'Ginecológicos', img: 'assets/img/medicamentos-ginecologicos.webp', route: '#/portafolio-ginecologicos' },
      { label: 'Cardiovasculares', img: 'assets/img/medicamentos-cardiovasculares.webp', route: '#/portafolio-cardiovasculares' },
      { label: 'Músculo-esquelético', img: 'assets/img/musculo-esqueleticos.webp', route: '#/portafolio-musculo-esqueleticos' },
      { label: 'Corticoesteroides', img: 'assets/img/medicamentos-corticoesteroides.webp', route: '#/portafolio-corticoesteroides' },
      { label: 'Hierros', img: 'assets/img/medicamento-hierro.webp', route: '#/portafolio-hierros' }
    ]
  },

  cuidado: {
    kicker: 'Cuidado de la salud',
    title: 'Medicamentos de venta libre',
    intro: 'Conoce a detalle toda la información de nuestro portafolio de productos de venta libre.',
    cards: [
      { id: 'gripe-y-resfriado', label: 'Gripe y resfriado', img: 'assets/img/gripe-y-resfriado-medicamento-chinoin.webp' },
      { id: 'tos', label: 'Tos', img: 'assets/img/tos-medicamento-chinoin.webp' },
      { id: 'piojos', label: 'Piojos', img: 'assets/img/piojos-medicamento-chinoin.webp' },
      { id: 'acidez-estomacal', label: 'Acidez estomacal', img: 'assets/img/acidez-estomacal-medicamento-chinoin.webp' },
      { id: 'diarrea', label: 'Diarrea', img: 'assets/img/diarrea-medicamentos-chinoin.webp' },
      { id: 'estrenimiento', label: 'Estreñimiento', img: 'assets/img/estrenimiento-medicamentos-chinoin.webp' },
      { id: 'sarna', label: 'Sarna', img: 'assets/img/sarna-medicamentos-chinoin.webp' },
      { id: 'fiebre-y-dolor', label: 'Fiebre y dolor', img: 'assets/img/fiebre-y-dolor-chinoin-medicamentos.webp' }
    ]
  },

  // Portafolios: logotipos de cada marca, como en el original.
  // prod = id en el catálogo (para abrir su ficha); href = enlace "Ver Más" del original.
  portafolios: {
    respiratorios: {
      title: 'Respiratorios', intro: 'Conoce nuestro portafolio de productos contra enfermedades respiratorias',
      items: [
        { name: 'Aytugre NS®', logo: 'assets/img/aytugrens.svg', prod: 'aytugre' },
        { name: 'Gabirol®', logo: 'assets/img/gabirol.svg' },
        { name: 'Koptin®', logo: 'assets/img/koptin.svg', prod: 'koptin-suspension' },
        { name: 'PilefhiD®', logo: 'assets/img/pilefhid.svg' },
        { name: 'Troferit® Flow', logo: 'assets/img/troferit-flow.webp' },
        { name: 'ZyXem®', logo: 'assets/img/zyxem-1.svg' },
        { name: 'Gotinal®', logo: 'assets/img/2.webp', prod: 'gotinal-adulto' }
      ]
    },
    gastrointestinales: {
      title: 'Gastrointestinales', intro: 'Conoce nuestro portafolio de productos contra enfermedades gastrointestinales',
      items: [
        { name: 'Norutec®', logo: 'assets/img/norutec-logo.webp' },
        { name: 'Talnesis®', logo: 'assets/img/chinoin-logos.svg' }
      ]
    },
    ginecologicos: {
      title: 'Medicamentos ginecológicos', kicker: 'Portafolio', intro: 'Conoce nuestro portafolio de productos contra enfermedades ginecológicas.',
      items: [{ name: 'Gitrasek®', logo: 'assets/img/gitrasek.svg' }]
    },
    cardiovasculares: {
      title: 'Cardiovasculares', intro: 'Conoce nuestro portafolio de productos contra enfermedades cardiovasculares.',
      items: [
        { name: 'Zathelo®', logo: 'assets/img/zathelo.svg' },
        { name: 'Gangotri®', logo: 'assets/img/gangotri.svg' }
      ]
    },
    'musculo-esqueleticos': {
      title: 'Músculo-esqueléticos', intro: 'Conoce nuestro portafolio de productos contra enfermedades músculo-esqueléticas.',
      items: [
        { name: 'Alin®', logo: 'assets/img/alin-1.webp', prod: 'alin-depot' },
        { name: 'Flexakocs®', logo: 'assets/img/flexacoks.webp', prod: 'flexakocs-capsulas' },
        { name: 'Mydocalm-A®', logo: 'assets/img/mydocalm-a.webp', prod: 'mydocalm-a-capsulas' },
        { name: 'Neuralin®', logo: 'assets/img/neuralin.webp' },
        { name: 'Neuralin Relief®', logo: 'assets/img/neuralin-relief.webp' },
        { name: 'Nevrika®', logo: 'assets/img/nevrika.webp' },
        { name: 'Reactix®', logo: 'assets/img/reactixs.webp' },
        { name: 'Sedepron®', logo: 'assets/img/sedepron.webp' },
        { name: 'Suma-B®', logo: 'assets/img/suma-b.webp' },
        { name: 'Trapazyd®', logo: 'assets/img/trapazyd-1.webp', prod: 'trapazyd-tabletas' },
        { name: 'Traumazol®', logo: 'assets/img/traumazol.webp' }
      ]
    },
    corticoesteroides: {
      title: 'Corticoesteroides', intro: 'Conoce nuestro portafolio de productos corticoesteroides.',
      items: [
        { name: 'Alin®', logo: 'assets/img/alin-1.webp', prod: 'alin-depot' },
        { name: 'Aytugre NS®', logo: 'assets/img/aytugrens.svg', prod: 'aytugre' },
        { name: 'Synalar®', logo: 'assets/img/synalar.webp' },
        { name: 'Topsyn®', logo: 'assets/img/topsyn.webp' }
      ]
    },
    hierros: {
      title: 'Hierros', intro: 'Conoce nuestro portafolio de hierros.',
      items: [
        { name: 'Ferranina®', sub: 'Complex', logo: 'assets/img/ferranina-complex.webp', href: 'https://www.chinoin.com/es/ferranina-complex' },
        { name: 'Ferranina®', sub: 'Fol', logo: 'assets/img/ferranina-fol.webp', href: 'https://www.chinoin.com/es/ferranina-fol' },
        { name: 'Venoferrum®', sub: 'Solución', logo: 'assets/img/venoferrum.webp', href: 'https://www.chinoin.com/es/venoferrum' }
      ]
    },
    odontologia: {
      title: 'Odontología', intro: 'Conoce nuestro portafolio de productos para odontología.',
      items: [
        { name: 'Alin®', logo: 'assets/img/alin-1.webp', prod: 'alin-depot' },
        { name: 'Flexakocs®', logo: 'assets/img/flexacoks.webp', prod: 'flexakocs-capsulas' },
        { name: 'Koptin®', logo: 'assets/img/koptin.svg', prod: 'koptin-suspension' },
        { name: 'Mydocalm-A®', logo: 'assets/img/mydocalm-a.webp', prod: 'mydocalm-a-capsulas' },
        { name: 'Neoseverin®', logo: 'assets/img/neoseverin-4.webp', prod: 'neoseverin-tabletas' },
        { name: 'Trapazyd®', logo: 'assets/img/trapazyd-1.webp', prod: 'trapazyd-tabletas' },
        { name: 'Reactix®', logo: 'assets/img/reactixs.webp' }
      ]
    },
    probioticos: {
      title: 'Probióticos', intro: 'Conoce nuestro portafolio de productos probióticos.',
      items: [
        { name: 'Benedual®', logo: 'assets/img/bene-dual.webp', prod: 'benei-dual-suspension' },
        { name: 'BeneI-G®', logo: 'assets/img/benei-g.webp', prod: 'benei-g-capsulas' },
        { name: 'Bene Quer®', logo: 'assets/img/bene-quer.webp', prod: 'bene-quer-polvo' }
      ]
    }
  },

  // Productos con ficha completa en chinoin.com (js/fichas.js)
  fichasPorProducto: {
    'neoseverin-tabletas': ['neoseverin-tabletas'],
    'neoseverin-suspension': ['neoseverin-suspension', 'neoseverin-suspension-ipp'],
    'scabisan-crema': ['scabisan-crema'],
    'scabisan-emulsion': ['scabisan-emulsion']
  },
  // Fichas que existen en chinoin.com pero no aparecen en el catálogo
  fichasSueltas: [
    { id: 'sunderin-tableta', name: 'Sunderin® Tableta', ficha: 'sunderin-tableta' },
    { id: 'zymir-ab-suspension', name: 'Zymir-AB® Suspensión', ficha: 'zymir-ab-suspension' }
  ],

  // Veterinaria: contenido de chinoinveterinaria.com/sitio (portada, contacto y apps).
  // Productos, fichas, empresa e historia están en js/veterinaria.js (generado con tools/veterinaria.py).
  veterinaria: {
    title: 'Veterinaria',
    sitio: 'https://chinoinveterinaria.com/sitio/',
    slogan: 'Chinoin Veterinaria al servicio de la salud y bienestar animal.',
    firma: 'Experiencia que da Vida',
    intro: 'Dirigido al desarrollo, fabricación y comercialización de productos para la salud animal, destacando su participación principalmente en: Bovinos, Ovinos, Caprinos, Porcinos, Equinos y Pequeñas Especies.',
    cta: 'Conoce los productos.',
    pilares: [
      { t: 'CHINOIN', p: 'Es una empresa orgullosamente mexicana dedicada al desarrollo, fabricación y comercialización de medicamentos de línea humana y veterinaria' },
      { t: 'Calidad', p: 'Contamos con los más altos estándares de calidad' },
      { t: 'Tecnología', p: 'Utilizamos tecnología de punta en la elaboración de nuestros productos' },
      { t: 'Pasión', p: 'Pasión y dedicación, ingredientes en nuestras fórmulas.' },
      { t: 'Nuestro futuro', p: 'Trabajar intensamente en la búsqueda de nuevos productos que enriquezcan nuestras líneas de negocio' }
    ],
    historiaTitle: '92 AÑOS CRECIENDO',
    lanzamientos: 'Lanzamientos recientes',
    lineas: [
      { id: 'pequenas-farmaceutica', grupo: 'Pequeñas Especies', linea: 'Farmacéutica' },
      { id: 'pequenas-oftalmicos', grupo: 'Pequeñas Especies', linea: 'Oftálmicos' },
      { id: 'pequenas-vacunas', grupo: 'Pequeñas Especies', linea: 'Vacunas' },
      { id: 'grandes-farmaceutica', grupo: 'Grandes Especies', linea: 'Farmacéutica' },
      { id: 'grandes-biologicos', grupo: 'Grandes Especies', linea: 'Biológicos' }
    ],
    especies: [
      { id: 'bovinos', label: 'Bovinos' }, { id: 'ovinos', label: 'Ovinos' }, { id: 'caprinos', label: 'Caprinos' },
      { id: 'porcinos', label: 'Porcinos' }, { id: 'equinos', label: 'Equinos' }, { id: 'caninos', label: 'Caninos' }, { id: 'felinos', label: 'Felinos' }
    ],
    contacto: {
      ventas: { label: 'Ventas', value: '01-800-907-4900', href: 'tel:018009074900' },
      gerencia: { label: 'Gerencia médica', value: '55-5262-3173', href: 'tel:+525552623173' },
      email: 'gervet@chinoin.com',
      direccion: 'Carretera Pabellón de Hidalgo km. 4.2 Municipio Rincón de Romos, 20420 Aguascalientes, Ags.'
    },
    app: {
      title: 'APP del Dolor', sub: 'Dolor en pequeñas especies', href: 'https://chinoinveterinaria.com/app',
      stores: [
        { label: 'App Store', href: 'https://itunes.apple.com/us/app/chinoin-veterinaria/id1329764781?l=es&ls=1&mt=8' },
        { label: 'Google Play', href: 'https://play.google.com/store/apps/details?id=com.chinoin.Animales_AR' }
      ]
    },
    social: [
      { label: 'Facebook', href: 'https://www.facebook.com/ChinoinProductosFarmaceuticos' },
      { label: 'X', href: 'https://twitter.com/ChinoinPF', icon: 'x' },
      { label: 'YouTube', href: 'https://www.youtube.com/channel/UC3SguU-Dc1L61rFbBm8Lbww', icon: 'youtube' }
    ],
    // Fotos de mascotas (Unsplash) para dar calidez a la sección
    fotos: {
      hero: 'assets/img/vet/corgi.webp',
      galeria: [
        'assets/img/vet/golden.webp', 'assets/img/vet/perro-gato.webp', 'assets/img/vet/beagle.webp', 'assets/img/vet/gatito.webp',
        'assets/img/vet/perros-corriendo.webp', 'assets/img/vet/samoyedo.webp', 'assets/img/vet/schnauzer.webp', 'assets/img/vet/gato.webp',
        'assets/img/vet/cachorro.webp', 'assets/img/vet/pastor.webp'
      ]
    }
  },

  footer: {
    about: 'Empresa orgullosamente mexicana, con 100 años de experiencia, dedicada al desarrollo, fabricación y comercialización de medicamentos con demostrada calidad, eficacia y seguridad.',
    logo: 'assets/img/logo-chinoin-experiencia-que-da-vida-full-color.webp',
    cols: [
      {
        title: 'Productos',
        links: [
          { label: 'Áreas terapéuticas', route: '#/medicamentos-prescripcion' },
          { label: 'Cuidado de la salud', route: '#/cuidado-de-la-salud' },
          { label: 'Probióticos', route: '#/probioticos' },
          { label: 'Odontología', route: '#/odontologia' },
          { label: 'Veterinaria', route: '#/veterinaria' }
        ]
      },
      {
        title: 'Otros enlaces',
        links: [
          { label: 'Reporte de farmacovigilancia', route: '#/farmacovigilancia' },
          { label: 'Biblioteca virtual', route: '#/biblioteca-virtual' },
          { label: 'Únete al equipo', route: '#/unete-al-equipo' },
          { label: 'Contacto', route: '#/contacto' }
        ]
      }
    ],
    direcciones: [
      { title: 'Planta en Aguascalientes:', text: 'Carretera Pabellón de Hidalgo km. 4.2, Municipio Rincón de Romos, 20420 Aguascalientes.' },
      { title: 'Oficinas generales y planta en México:', text: 'Lago Tangañica #18, Colonia Granada, 11520 México, CDMX.' }
    ],
    tel: 'Tel. 52 (465) 9581804 / Fax: 52(55) 5531 43 49',
    email: 'ventas@chinoin.com',
    copy: 'CHINOIN® 2025. Todos los derechos reservados.',
    cofepris: 'Registro COFEPRIS: 213300201B3210. Consulte a su médico.'
  }
};
