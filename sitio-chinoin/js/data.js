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
      gallery: [
        { src: 'assets/img/instalaciones-11-390x260.webp', alt: 'tecnología farmacéutica' },
        { src: 'assets/img/instalaciones-13-390x260.webp', alt: 'tecnología farmacéutica' },
        { src: 'assets/img/instalaciones-15-390x260.webp', alt: 'farmaceutica mexicana' },
        { src: 'assets/img/instalaciones-18-390x260.webp', alt: 'tecnología farmacéutica' },
        { src: 'assets/img/instalaciones-17-390x260.webp', alt: 'Instalaciones' },
        { src: 'assets/img/instalaciones-16-390x260.webp', alt: 'Instalaciones' },
        { src: 'assets/img/almacen-chinoin-video.webp', alt: 'almacen-chinoin-video', video: 'https://www.youtube.com/watch?v=J_RZoEkLuq4&t=11s' }
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

  // Veterinaria: en el original el menú abre chinoinveterinaria.com en otra pestaña.
  veterinaria: {
    title: 'Veterinaria',
    // Textos de chinoin.com que hablan de la línea veterinaria
    citas: [
      'El Círculo Dorado de Chinoin® forma parte de nuestra cultura y ADN, lo que nos impulsa día a día a brindar soluciones terapéuticas con precio justo para cada uno de nuestros clientes de las diferentes líneas humana y veterinaria con las que contamos.',
      'Contamos con la capacidad, instalaciones y tecnología avanzada para la fabricación de productos, tanto para uso humano como veterinario.'
    ],
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
