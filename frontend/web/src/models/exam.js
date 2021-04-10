import {
    createExamPaper,
    getExamPaper,
    listExamPaper,
} from '@/services/services';

export default {
    namespace: 'exam',

    state: {
        data: {
            list: [],
            total: 0,
        },
    },

    effects: {
        *listExamPaper({ payload }, { call, put }) {
            const resp = yield call(listExamPaper, payload);
            yield put({
                type: 'saveExamPaperList',
                payload: resp
            });
            return resp;
        },
        *createExamPaper({ payload }, { call, put }) {
            return yield call(createExamPaper, payload);
        },
        *getExamPaper({ payload }, { call, put }) {
            return yield call(getExamPaper, payload);
        },
    },

    reducers: {
        saveExamPaperList(state, action) {
            return {
                ...state,
                data: {
                    list: action.payload.data,
                    total: action.payload.total,
                }
            };
        }
    }
}