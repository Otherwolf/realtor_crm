import axios from 'axios'

axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.auth = {username: 'test@mail.ru', password: 'qwerty123'}
axios.defaults.xsrfCookieName = 'csrftoken'

export default axios.create({baseURL: '/rest/', timeout: 100000})


