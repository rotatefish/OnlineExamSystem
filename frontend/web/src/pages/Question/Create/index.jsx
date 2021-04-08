import React, { PureComponent } from 'react';
import ProForm, {
  ProFormSwitch,
  ProFormText,
  ProFormRadio,
  ProFormCheckbox,
  ProFormRate,
  ProFormDatePicker,
  ProFormSelect,
  ProFormDigit,
  ProFormDateTimePicker,
  ProFormSlider,
  ProFormDateTimeRangePicker,
  ProFormDateRangePicker,
  ProFormUploadButton,
  ProFormUploadDragger,
  ProFormFieldSet,
  ProFormTimePicker,
  ProFormList,
  ProFormDependency,
  StepsForm,
} from '@ant-design/pro-form';
import { PageContainer } from '@ant-design/pro-layout';
import { message } from 'antd';
import { connect } from 'umi';
import ProCard from '@ant-design/pro-card';


const initQuestionType = 'SINGLE';
const questionType = [
  {
    label: '单选题',
    value: 'SINGLE',
  },
  {
    label: '多选题',
    value: 'MULTIPLE',
  },
  {
    label: '判断题',
    value: 'JUDGE',
  },
];
const initSelectList = [
  {
    option: 'A'
  },
  {
    option: 'B'
  },
  {
    option: 'C'
  },
  {
    option: 'D'
  },
]

@connect(({ question }) => ({
  question
}))
class CreateChoiceQuestion extends PureComponent {

  handleCreate = async (values) => {
    message.success('开始创建');
    if (values.questionType === 'JUDGE') {
      message.info('判断题');
      const resp = await this.props.dispatch({
        type: 'question/createJudgeQuestion',
        payload: {
          description: values.description,
          answser: values.judgeAnswser
        }
      });
      if (resp) {
        message.info('判断题创建成功');
      }
    } else {
      const resp = await this.props.dispatch({
        type: 'question/createChoiceQuestion',
        payload: {
          type: values.questionType,
          description: values.description,
          singleAnswser: values.singleAnswser,
          multipleAnswser: values.multipleAnswser,
          contents: values.optionContent
        }
      });
      if (resp) {
        message.info('创建成功');
      }
    }
  }

  handleTypeChange = value => {
    this.setState({ type: value });
  }

  render() {
    return (
      <PageContainer>
        <ProCard
          style={{
            padding: 100,
          }}
        >
          <ProForm
            name="create_question"
            onValuesChange={(_, values) => {
              console.log(values);
            }}
            onFinish={values => this.handleCreate(values)}
          >
            <ProFormRadio.Group
              name="questionType"
              label="题目类型"
              radioType="button"
              initialValue={initQuestionType}
              rules={[{ required: true, message: '请选择题目类型' }]}
              options={questionType}
            />
            <ProFormText
              width="lg"
              name="description"
              label="题目描述"
              rules={[{ required: true, message: '请输入题目描述' }]}
            />
            <ProFormDependency name={['questionType']}>
              {({ questionType }) => {
                if (questionType === 'SINGLE' || questionType === 'MULTIPLE') {
                  return (
                    <ProFormList
                      name="optionContent"
                      label="问题选项"
                      rules={[{ required: true, message: '请增加问题选项' }]}
                      creatorButtonProps={{
                        creatorButtonText: '新增选项'
                      }}
                      initialValue={initSelectList}
                    >
                      <ProForm.Group>
                        <ProFormSelect
                          name="option"
                          label="选项"
                          valueEnum={["A", "B", "C", "D", "E"]}
                          rules={[{ required: true, message: '请选择选项标号' }]}
                        >
                        </ProFormSelect>
                        <ProFormText
                          name="data"
                          label="内容"
                          rules={[{ required: true, message: '请输入选项内容' }]}
                        />
                      </ProForm.Group>
                    </ProFormList>
                  )
                }
              }}
            </ProFormDependency>
            <ProFormDependency name={['questionType']}>
              {({ questionType }) => {
                if (questionType === 'SINGLE') {
                  return (
                    <ProFormRadio.Group
                      name="singleAnswser"
                      label="答案"
                      rules={[{ required: true, message: '请选择答案' }]}
                      options={[
                        {
                          label: 'A',
                          value: 'A',
                        },
                        {
                          label: 'B',
                          value: 'B',
                        },
                        {
                          label: 'C',
                          value: 'C',
                        },
                        {
                          label: 'D',
                          value: 'D',
                        },
                      ]}
                    />
                  );
                } else if (questionType === 'MULTIPLE') {
                  return (
                    <ProFormCheckbox.Group
                      name="multipleAnswser"
                      label="答案"
                      options={['A', 'B', 'C', 'D']}
                      rules={[{ required: true, message: '请选择答案' }]}
                    />
                  )
                } else if (questionType === 'JUDGE') {
                  return (
                    <ProFormRadio.Group
                      name='judgeAnswser'
                      label='判断题答案'
                      rules={[{ required: true, message: '请选择答案' }]}
                      options={[
                        {
                          label: '正确',
                          value: true
                        },
                        {
                          label: '错误',
                          value: false
                        }
                      ]}
                    >
                    </ProFormRadio.Group>
                  )
                }
              }}
            </ProFormDependency>
          </ProForm>
        </ProCard>
      </PageContainer >
    );
  }
}

export default CreateChoiceQuestion;