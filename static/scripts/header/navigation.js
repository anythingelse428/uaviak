const createHeaderNavigation = (selector, links) => Vue.createApp({
    data() {
        return {
            links: links,
            menu: {
                mainLinks: [],
                subLinks: {
                    links:[],
                    isOpen: false
                },
            }
        }
    },
    mounted() {
        this.breakpoints();
    },
    created() {
        this.breakpoints();
        window.addEventListener('resize', this.breakpoints);
    },
    destroyed() {
        window.removeEventListener('resize', this.breakpoints);
    },
    methods: {
        breakpoints() {
            const width = document.querySelector(selector).offsetWidth
            if (width <= 800) {
                this.menu.mainLinks = []
                this.menu.subLinks = { links: [...this.links], isOpen: false }
            } else if (width <= 900) {
                this.menu.mainLinks = this.links.slice(0, 4)
                this.menu.subLinks = { links: [...this.links].slice(4, this.links.length), isOpen: false }
            } else if (width <= 1000) {
                this.menu.mainLinks = this.links.slice(0, 5)
                this.menu.subLinks = { links: [...this.links].slice(5, this.links.length), isOpen: false }
            } else if (width <= 1240) {
                this.menu.mainLinks = this.links.slice(0, 6)
                this.menu.subLinks = { links: [...this.links].slice(6, this.links.length), isOpen: false }
            } else {
                this.menu.mainLinks = this.links.slice(0, 9)
                this.menu.subLinks = { links: [...this.links].slice(9, this.links.length), isOpen: false }
            }




        },
        closeAllLinksGroups(arr) {
            arr.forEach(el => {
                    el.isOpen = false
            });

        },
        toggleLinksGroupVisibility(arr, index) {
            if (arr[index].isOpen) {
                return arr[index].isOpen = false
                // закрываю по нажатию на уже открытое
            }

            this.closeAllLinksGroups(arr)
            arr[index].isOpen = !arr[index].isOpen

        },
        toggleMenuVisibility() {
            this.closeAllLinksGroups(this.menu.mainLinks)
            this.closeAllLinksGroups(this.menu.subLinks.links)

            this.menu.subLinks.isOpen = !this.menu.subLinks.isOpen
        },

    },
    delimiters: ['[[', ']]']
}).mount(selector)