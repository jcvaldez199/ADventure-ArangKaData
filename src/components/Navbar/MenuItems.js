import { Home } from '../Home/Home'
import { Customer } from '../Customer/Customer'
import { Video } from '../Video/Video'
import { Request } from '../Request/Request'
import { Register } from '../Register/Register'

export const MenuItems = [
    {
        title: 'Home',
        url: '/',
        comp: Home,
        cName: 'nav-links'
    },
    {
        title: 'Profile',
        url: '/customer',
        comp: Customer,
        cName: 'nav-links'
    },
    {
        title: 'Manage Videos',
        url: '/videos',
        comp: Video,
        cName: 'nav-links'
    },
    {
        title: 'Requests',
        url: '/request',
        comp: Request,
        cName: 'nav-links'
    },
    {
        title: 'Register',
        url: '/register',
        comp: Register,
        cName: 'nav-links'
    },
]
