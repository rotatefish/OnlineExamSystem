import { PageContainer } from '@ant-design/pro-layout';
import React, { useState, useRef, PureComponent } from 'react';
import { message, Button } from 'antd';
import ProTable from '@ant-design/pro-table';
import { EditableProTable } from '@ant-design/pro-table';
import ProForm, { ModalForm, ProFormText, ProFormTextArea } from '@ant-design/pro-form';
import { connect, FormattedMessage, Link, history } from 'umi';
import { PlusOutlined } from '@ant-design/icons';


const columns = [
  {
    title: '题目ID',
    dataIndex: 'id',
    sorter: (a, b) => b - a,
  },
  {
    title: '题目描述',
    dataIndex: 'description',
    copyable: true,
  },
];

@connect(({ question }) => ({
  question
}))
class QuestionList extends PureComponent {

  state = {
    createModalVisible: false,
  }
  async componentDidMount() {

    // const resp = this.props.dispatch({
    //   type: 'question/queryQuestionList'
    // });
    // const values = await Promise.all([resp]);
    // if (values) {
    //   message.success('success');
    // } else {
    //   message.error('failed');
    // }
  }

  getChoiceQuestionList = (params, sort, filter) => {
    const resp = this.props.dispatch({
      type: 'question/queryQuestionList',
      payload: {
        current: params.current,
        pageSize: params.pageSize,
        filters: {
          id: params.id,
          description: params.description,
        },
      }
    });
    return resp;
  }


  renderToolBar = () => {
    return [
      <Button
        type="primary"
        key="primary"
        onClick={() => {
          //this.handleCreateModalVisible(true);
          message.info('创建题目');
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

  renderPage = () => {

    return (
      <PageContainer>
        <ProTable
          headerTitle={'选择题列表'}
          columns={columns}
          request={(params, sort, filter) => this.getChoiceQuestionList(params, sort, filter)}
          toolBarRender={() => this.renderToolBar()}
        >

        </ProTable>
        <ModalForm
          title="新建题目"
          width="800px"
          visible={this.state.createModalVisible}
          onVisibleChange={this.handleCreateModalVisible}
          onFinish={() => this.handleAdd()}
        >
        </ModalForm>
      </PageContainer>
    );
  }

  render() {
    //console.log(this.props.question.data.list[0]);
    return this.renderPage();
  }
};

export default QuestionList;