import request from '@/utils/request';

export async function queryQuestionList(params) {
    return request('/api/v1/question/choice_question/list', {
        method: 'POST',
        data: params
    });
}

export async function createChoiceQuestion(params) {
    return request('/api/v1/question/choice_question/create', {
        method: 'POST',
        data: params
    });
}

export async function createJudgeQuestion(params) {
    return request('/api/v1/question/judge_question/create', {
        method: 'POST',
        data: params
    });
}
