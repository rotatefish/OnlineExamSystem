import {
    queryQuestionList,
    createChoiceQuestion,
    createJudgeQuestion,
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
        *queryQuestionList({ payload }, { call, put }) {
            const resp = yield call(queryQuestionList, payload);
            yield put({
                type: 'saveQuestionList',
                payload: resp
            });
            return resp;
        },
        *createChoiceQuestion({ payload }, { call, put }) {
            return yield call(createChoiceQuestion, payload);
        },
        *createJudgeQuestion({ payload }, { call, put }) {
            return yield call(createJudgeQuestion, payload);
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