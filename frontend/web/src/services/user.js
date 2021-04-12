import request from '@/utils/request';

export async function query() {
  return request('/api/users');
}

export async function queryCurrent() {
  return request('/api/currentUser');
}

export async function queryNotices() {
  return request('/api/notices');
}

export async function userLogin(params) {
  return request('/api/v1/user/login', {
    method: 'POST',
    data: params
  });
}

export async function userLogout(params) {
  return request('/api/v1/user/logout', {
    method: 'POST',
    data: params
  });
}

export async function currentUser() {
  return request('/api/v1/user/current');
}