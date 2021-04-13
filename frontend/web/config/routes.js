export default [
    {
        path: '/',
        component: '../layouts/BlankLayout',
        routes: [
            {
                path: '/user',
                component: '../layouts/UserLayout',
                routes: [
                    {
                        name: 'login',
                        path: '/user/login',
                        component: './User/login',
                    },
                ],
            },
            {
                path: '/',
                component: '../layouts/SecurityLayout',
                routes: [
                    {
                        path: '/',
                        component: '../layouts/BasicLayout',
                        authority: ['admin', 'user'],
                        routes: [
                            {
                                path: '/',
                                redirect: '/welcome',
                            },
                            {
                                path: '/welcome',
                                name: 'welcome',
                                icon: 'smile',
                                component: './Welcome',
                            },
                            {
                                path: '/admin',
                                name: 'admin',
                                icon: 'crown',
                                component: './Admin',
                                authority: ['admin'],
                                routes: [
                                    {
                                        path: '/admin/sub-page',
                                        name: 'sub-page',
                                        icon: 'smile',
                                        component: './Welcome',
                                        authority: ['admin'],
                                    },
                                ],
                            },
                            {
                                path: '/question',
                                name: 'question',
                                icon: 'crown',
                                routes: [
                                    {
                                        name: 'list',
                                        icon: 'smile',
                                        path: '/question/list',
                                        component: './Question/List/QuestionList',
                                    },
                                    {
                                        name: 'create',
                                        icon: 'smile',
                                        path: '/question/create',
                                        component: './Question/Create/CreateChoiceQuestion',
                                    },
                                ],
                            },
                            {
                                path: '/exam',
                                name: 'exam',
                                icon: 'cloud-server',
                                hideChildrenInMenu: true,
                                routes: [
                                    {
                                        path: '/exam',
                                        component: './Exam/ExamPaperList',
                                    },
                                    {
                                        path: '/exam/detail',
                                        component: './Exam/ExamPaperDetail',
                                    },
                                    {
                                        path: '/exam/create',
                                        component: './Exam/CreateExamPaper',
                                    },
                                ]
                            },
                            {
                                path: '/contest',
                                name: 'contest',
                                icon: 'cloud-server',
                                routes: [
                                    {
                                        path: '/contest',
                                        component: './Contest/ContestList'
                                    },
                                ]
                            },
                            {
                                name: 'userList',
                                path: '/userList',
                                icon: 'smile',
                                component: './User/UserList'
                            },
                            {
                                name: 'list.table-list',
                                icon: 'table',
                                path: '/list',
                                component: './TableList',
                            },
                            {
                                component: './404',
                            },
                        ],
                    },
                    {
                        component: './404',
                    },
                ],
            },
        ],
    },
    {
        component: './404',
    },
];
