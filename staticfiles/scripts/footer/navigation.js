const createFooterNavigation = selector => Vue.createApp({
    data() {
        return {
            accordion: {
                isOpen: false,
                classList: []
            }
        }
    },
    methods: {
        toggleAccordion() {
            try {
                if (this.accordion.isOpen) {
                    this.$refs.accordionContent.style.height = '0'
                    this.accordion.classList.length = 0
                } else {
                    // this.$refs.accordionContent.style.height = `${this.$refs.accordionContent.scrollHeight}px`
                    // хуита, ссылки уебывают под #footer-meta
                    this.accordion.classList.push('open')
                }
            } catch (err) {
                console.error(err)
            }
            this.accordion.isOpen = !this.accordion.isOpen
        }
    }
}).mount(selector)

/*
* Основные сведения
* Атлас профессий
* Расписание
* Стипендии
* МЦК
* Структура и органы управления
* Документы для приема
* График учебного процесса
* Правила внутреннего распорядка
* 3D тур
* Руководство и преподаватели
* Правила и порядок приема
* Платное обучение
* Студенту-дипломнику
* Вакансии
* Документы
* Перечень специальностей
* Подготовительные курсы
* Рекомендации студенту
* Контакты
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
* */