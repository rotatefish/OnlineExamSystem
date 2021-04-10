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
  ProFormFieldSet,
  ProFormList,
  ProFormDependency,
} from '@ant-design/pro-form';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, message, Divider, Spin } from 'antd';
import { connect, history } from 'umi';
import ProCard from '@ant-design/pro-card';
import ProList from '@ant-design/pro-list';


@connect(({ exam }) => ({
  exam
}))
class ExamPaperDetail extends PureComponent {


  state = {
    examPaper: null,
    questions: [],
  }

  componentDidMount = async () => {
    const resp = await this.props.dispatch({
      type: 'exam/getExamPaper',
      payload: {
        eId: this.props.location.state.eid
      }
    });
    if (resp) {
      this.setState({
        examPaper: resp.examPaper,
        questions: resp.questions,
      });
      message.info('预览试卷');
    } else {
    }
  }

  metas = {
    title: {
      dataIndex: '',
    }
  }

  render() {
    if (this.state.examPaper === null) return <Spin></Spin>
    console.log(this.state.examPaper);
    console.log(this.state.questions);

    const tmp = this.state.examPaper.title;
    message.info('debug');
    return (
      <PageContainer>
        <ProCard
          title={this.state.examPaper.title}
        >
          <ProForm
            name="finish_exam"
            onValuesChange={(_, values) => {
              console.log(values);
            }}
          >
            {
              this.state.questions.map((q, index) => {
                if (q.type === 'SINGLE') {
                  return (
                    <Card>
                      <ProFormRadio.Group
                        label={`第${index + 1}题. ${q.description}`}
                        name={`q${index}`}
                        layout="vertical"
                        initialValue={q.choiceData.singleAnswser}
                        options={
                          q.choiceData.contents.map(v => {
                            return {
                              label: `${v.option}. ${v.data}`,
                              value: v.option
                            }
                          })
                        }
                      >
                      </ProFormRadio.Group>
                    </Card>
                  )
                } else if (q.type === 'JUDGE') {
                  return (
                    <Card>
                      <ProFormRadio.Group
                        label={`第${index + 1}题. ${q.description} ?`}
                        name={`q${index}`}
                        layout="vertical"
                        initialValue={q.judgeData.answser}
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
                    </Card>
                  )
                }
              })
            }
          </ProForm>
        </ProCard>
      </PageContainer >
    );
  }
}

export default ExamPaperDetail;