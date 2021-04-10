import ProCard from '@ant-design/pro-card';
import { PageContainer } from '@ant-design/pro-layout';
import ProTable from '@ant-design/pro-table';
import React, { PureComponent } from 'react';




class ContestList extends PureComponent {


  columns = [
    {
      title: '考试编号',
    },
    {
      title: '考试标题',
    },
    {
      title: '考试状态',
    },
    {
      title: '考试时间',
    },
    {
      title: '创建时间',
    },
    {
      title: '更新时间',
    },
    {
      title: '创建者',
    },
    {
      title: '操作',
    }
  ];

  listEContest = (params, sort, filter) => {


  }
  render() {
    return (
      <PageContainer
        
      >
        <ProCard>
          <ProTable
            headerTitle={'考试列表'}
            columns={this.columns}
            request={(params, sort, filter) => this.listEContest(params, sort, filter)}
          >
          </ProTable>
        </ProCard>
      </PageContainer>
    )
  }
}

export default ContestList;