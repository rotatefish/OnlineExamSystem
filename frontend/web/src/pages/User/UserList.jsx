import ProCard from '@ant-design/pro-card';
import React, { PureComponent } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ProTable from '@ant-design/pro-table';
import { connect } from 'umi';
import { Avatar, Image, Button } from 'antd';

@connect(({ user }) => ({
    user
}))
class UserList extends PureComponent {

    columns = [
        {
            title: '头像',
            dataIndex: 'avatar',
            render: (data, record, index) => {
                return <Avatar
                    src={data}
                ></Avatar>
            }
        },
        {
            title: '学号',
            dataIndex: 'userId',
            tip: '学号是唯一的'
        },
        {
            title: '姓名',
            dataIndex: 'name',
        },
        {
            title: '权限',
            dataIndex: 'role'
        },
        {
            title: '邮箱',
            dataIndex: 'email',
        },
        {
            title: '性别',
            dataIndex: 'gender',
        },
        {
            title: '密码',
            dataIndex: 'password',
        },
        {
            title: '操作',
            render: (data, record, index) => {
                return <div>
                    <Button>
                        修改权限
                    </Button>
                </div>
            }
        }
    ];

    queryAllUser = (params, sort, filter) => {
        const resp = this.props.dispatch({
            type: 'user/queryAllUser',
            payload: {
                current: params.current,
                pageSize: params.pageSize,
                filters: {
                    userId: params.userId,
                    name: params.name,
                    role: params.role,
                    gender: params.gender,
                }
            }
        });
        return resp;
    }

    render() {
        return (
            <PageContainer>
                <ProCard
                >
                    <ProTable
                        headerTitle={'用户列表'}
                        columns={this.columns}
                        request={(params, sort, filter) => this.queryAllUser(params, sort, filter)}
                    >

                    </ProTable>
                </ProCard>
            </PageContainer>
        )
    }
}

export default UserList;
