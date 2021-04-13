import {
  queryCurrent,
  query as queryUsers,
  userLogin,
  userLogout,
  currentUser,
  queryAllUser,
} from '@/services/user';
import { history } from 'umi';
import { message } from 'antd';
import { setAuthority } from '@/utils/authority';
import { getPageQuery } from '@/utils/utils';

const UserModel = {
  namespace: 'user',
  state: {
    currentUser: {},
  },
  effects: {
    *fetch(_, { call, put }) {
      const response = yield call(queryUsers);
      yield put({
        type: 'save',
        payload: response,
      });
    },

    *fetchCurrent(_, { call, put }) {
      const response = yield call(currentUser);
      yield put({
        type: 'saveCurrentUser',
        payload: response,
      });
    },
    *login({ payload }, { call, put }) {
      const response = yield call(userLogin, payload);
      yield put({
        type: 'changeLoginStatus',
        payload: response
      });

      if (response) {
        const urlParams = new URL(window.location.href);
        const params = getPageQuery();
        message.success('🎉 🎉 🎉  登录成功！');
        let { redirect } = params;

        if (redirect) {
          const redirectUrlParams = new URL(redirect);

          if (redirectUrlParams.origin === urlParams.origin) {
            redirect = redirect.substr(urlParams.origin.length);

            if (window.routerBase !== '/') {
              redirect = redirect.replace(window.routerBase, '/');
            }

            if (redirect.match(/^\/.*#/)) {
              redirect = redirect.substr(redirect.indexOf('#') + 1);
            }
          } else {
            window.location.href = '/';
            return;
          }
        }

        history.replace(redirect || '/');
      }
    },
    *logout({ payload }, { call }) {
      const { redirect } = getPageQuery();
      const response = yield call(userLogout, payload);
      if (response) {
        message.success('成功登出');
      }
      history.push('/user/login');
      if (window.location.pathname !== '/user/login' && !redirect) {
        history.replace({
          pathname: '/user/login',
          search: stringify({
            redirect: window.location.href,
          }),
        });
      }
    },
    *queryAllUser({ payload }, { call, put }) {
      const response = yield call(queryAllUser, payload);

      return response;
    }
  },
  reducers: {
    saveCurrentUser(state, action) {
      return { ...state, currentUser: action.payload || {} };
    },

    changeLoginStatus(state, action) {
      setAuthority('admin');
      return { ...state, status: 'ok', type: 'account' };
    },

    changeNotifyCount(
      state = {
        currentUser: {},
      },
      action,
    ) {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          notifyCount: action.payload.totalCount,
          unreadCount: action.payload.unreadCount,
        },
      };
    },
  },
};
export default UserModel;
