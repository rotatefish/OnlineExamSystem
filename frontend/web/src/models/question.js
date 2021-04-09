import {
    createQuestion,
    listAllQuestions,
} from '@/services/services';


export default {
    namespace: 'question',

    state: {
        data: {
            list: [],
            total: 0,
        },
    },

    effects: {
        *listAllQuestions({ payload }, { call, put }) {
            const resp = yield call(listAllQuestions, payload);
            yield put({
                type: 'saveQuestionList',
                payload: resp
            });
            return resp;
        },
        *createQuestion({ payload }, { call, put }) {
            return yield call(createQuestion, payload);
        },
    },

    reducers: {
        saveQuestionList(state, action) {
            return {
                ...state,
                data: {
                    list: action.payload.data,
                },
            };
        }
    }
};