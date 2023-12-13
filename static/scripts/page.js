const createPage = (selector, tabs) => Vue.createApp({
    data() {
        return {
            subPages: tabs
        }
    },
    mounted() {
        if (window.location.hash) this.selectSubPage(window.location.hash.replace('#', ''))
        if (this.subPages.filter(subPage => subPage.isActive).length === 0 && this.subPages.length !== 0) {
            this.subPages[0] = {
                ...this.subPages[0],
                isActive: true
            }
        }
    },
    computed: {
        currentSubPage() {
            return this.subPages.find(subPage => subPage.isActive)
        }
    },
    methods: {
        selectSubPage(id) {
            this.subPages = this.subPages.map(subPage => ({
                ...subPage,
                isActive: id === subPage.id
            }))
            window.location.hash = `#${id}`
        }
    },
    delimiters: ['[[', ']]']
}).mount(selector)
