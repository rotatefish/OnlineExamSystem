import { PageContainer } from '@ant-design/pro-layout';
import React, { useState, useRef, PureComponent } from 'react';
import { message, Button, Tag, Tabs } from 'antd';
import ProTable from '@ant-design/pro-table';
import { EditableProTable } from '@ant-design/pro-table';
import ProForm, { DrawerForm, ModalForm, ProFormText, ProFormTextArea } from '@ant-design/pro-form';
import { connect, FormattedMessage, Link, history } from 'umi';
import { PlusOutlined } from '@ant-design/icons';
import moment from 'moment';
import ProCard from '@ant-design/pro-card';

@connect(({ question }) => ({
  question
}))
class QuestionList extends PureComponent {

  state = {
    createModalVisible: false,
  }

  columns = [
    {
      title: '题目编号',
      dataIndex: 'qId',
      sorter: (a, b) => b - a,
    },
    {
      title: '题目描述',
      dataIndex: 'description',
      copyable: true,
    },
    {
      title: '问题类型',
      dataIndex: 'type',
      valueEnum: {
        UNKNOWN: {
          text: '全部',
        },
        SINGLE: {
          text: '单选题',
        },
        MULTIPLE: {
          text: '多选题',
        },
        JUDGE: {
          text: '判断题',
        },
      },
    },
    {
      title: '问题答案',
      render: (data, record) => {
        console.log(record);
        const type = record.type;
        if (type === 'SINGLE') {
          return record.choiceData.singleAnswser;
        } else if (type === 'MULTIPLE') {
          return record.choiceData.multipleAnswser;
        } else if (type === 'JUDGE') {
          if (record.judgeData.answser) {
            return 'true';
          } else {
            return 'false';
          }
        }
      }
    },
    {
      title: '问题状态',
      dataIndex: 'status',
      dataType: 'select',
      valueEnum: {
        UNKNOWN: {
          text: '未知',
          status: 'Default'
        },
        ENABLED: {
          text: '正常',
          status: 'Success',
        },
        DISABLED: {
          text: '禁用',
          status: 'Error',
        }
      },
    },
    {
      title: '创建时间',
      dataIndex: 'creationTime',
      render: (data, record, index) => {
        return <span>{moment(new Date(parseInt(data * 1000))).format('YYYY-MM-DD HH:mm:ss')}</span>;
      }
    },
    {
      title: '创建者',
      dataIndex: 'createdBy',
    },
    {
      title: '操作',
      render: (data, record) => {
        return (
          <div>
            <Button type="link">禁用</Button>
            <ModalForm
              trigger={
                <Button>修改</Button>
              }
              onFinish={
                (values) => {
                  this.handleUpdate(values);
                  return true;
                }
              }
            >
              
            </ModalForm>
            <DrawerForm
              trigger={
                <Button>详情</Button>
              }
            ></DrawerForm>
          </div>
        )
      }
    }
  ];

  handleUpdate = values => {

  }

  getQuestionList = (params, sort, filters) => {
    const resp = this.props.dispatch({
      type: 'question/listAllQuestions',
      payload: {
        current: params.current,
        pageSize: params.pageSize,
        filters: {
          qId: params.qId,
          type: params.type,
          description: params.description,
        }
      },
    });
    return resp;
  }

  renderToolBar = () => {
    return [
      <Button
        type="primary"
        key="primary"
        onClick={() => {
          history.push('/question/create');
        }}
      >
        <Link to="/question/create"></Link>
        <PlusOutlined />
        <FormattedMessage id="pages.searchTable.new" defaultMessage="新建" />
      </Button>,
    ]
  }


  handleCreateModalVisible = (value) => {
    this.setState({ createModalVisible: value });
  }
  handleAdd = () => {
    this.handleCreateModalVisible(false);
    message.success('添加成功');
  }

  render() {
    return (
      <PageContainer>
        <ProCard>
          <ProTable
            headerTitle={'题目列表'}
            columns={this.columns}
            request={(params, sort, filter) => this.getQuestionList(params, sort, filter)}
            toolBarRender={() => this.renderToolBar()}
          >
          </ProTable>
        </ProCard>
      </PageContainer>
    );
  }
};

export default QuestionList;