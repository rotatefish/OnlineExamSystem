import { PageContainer } from '@ant-design/pro-layout';
import React, { useState, useEffect, PureComponent } from 'react';
import { Spin } from 'antd';
import styles from './ExamPaperList.less';
import ProCard from '@ant-design/pro-card';
import ProTable from '@ant-design/pro-table';
import { filter } from 'lodash-es';
import { message, Button, Tag, Tabs } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { connect, FormattedMessage, Link, history } from 'umi';
import moment from 'moment';



@connect(({ exam }) => ({
  exam
}))
class ExamPaperList extends PureComponent {

  columns = [
    {
      title: '试卷编号',
      dataIndex: 'eId',
    },
    {
      title: '试卷标题',
      dataIndex: 'title',
    },
    {
      title: '创建时间',
      dataIndex: 'creationTime',
      render: (data, record, index) => {
        return <span>{moment(new Date(parseInt(data * 1000))).format('YYYY-MM-DD HH:mm:ss')}</span>;
      },
    },
    {
      title: '创建者',
      dataIndex: 'createdBy',
    },
    {
      title: '状态',
      dataIndex: 'status',
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
      title: '操作',
      render: (data, record, index) => {
        return <div>
          <Button type="link" onClick={() => history.push({ pathname: '/exam/detail', state: { eid: data.eId } })}>详情</Button>
          <Button type="link">修改</Button>
          <Button type="primary" color="red">禁用</Button>
        </div>
      }
    }
  ];

  listExamPapers = (params, sort, filter) => {
    console.log(params);
    const resp = this.props.dispatch({
      type: 'exam/listExamPaper',
      payload: {
        current: params.current,
        pageSize: params.pageSize,
        filters: {
          eId: params.eId,
          title: params.title,
        }
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
          history.push('/exam/create');
        }}
      >
        <PlusOutlined />
        新建
      </Button>,
    ]
  }

  render() {
    return (
      <PageContainer>
        <ProCard>
          <ProTable
            headerTitle={'试卷列表'}
            columns={this.columns}
            request={(params, sort, filter) => this.listExamPapers(params, sort, filter)}
            toolBarRender={() => this.renderToolBar()}
          >

          </ProTable>
        </ProCard>
      </PageContainer>
    )
  }
}

export default ExamPaperList;