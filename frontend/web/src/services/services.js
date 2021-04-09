import request from '@/utils/request';

// question
export async function createQuestion(params) {
    console.log('start');
    return request('/api/v1/question/all_question/create', {
        method: 'POST',
        data: params
    });
}

export async function listAllQuestions(params) {
    return request('/api/v1/question/all_question/list', {
        method: 'POST',
        data: params
    });
}

// exam paper
export async function createExamPaper(params) {
    return request('/api/v1/exam/exam_paper/create', {
        method: 'POST',
        data: params
    });
}

export async function getExamPaper(params) {
    return request('/api/v1/exam/exam_paper/get', {
        method: 'POST',
        data: params
    });
}

export async function listExamPaper(params) {
    return request('/api/v1/exam/exam_paper/list', {
        method: 'POST',
        data: params
    });
}