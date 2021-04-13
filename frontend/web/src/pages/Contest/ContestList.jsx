import ProCard from '@ant-design/pro-card';
import { PageContainer } from '@ant-design/pro-layout';
import ProTable from '@ant-design/pro-table';
import React, { PureComponent } from 'react';
import { Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import ProForm, {
    ModalForm,
    ProFormText,
    ProFormTimePicker,
    ProFormDatePicker,
    ProFormSelect
} from '@ant-design/pro-form';
import {connect} from 'umi';


@connect(({ exam }) => ({
    exam
}))
class ContestList extends PureComponent {

    state = {
        CreateContestVisiale: false
    }

    componentDidMount() {

    }

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

    handleCreateContestVisiale = value => {
        this.setState({ CreateContestVisiale: value });
    }

    handleAddContest = values => {

        return true;
    }

    renderToolBar = () => {
        return [
            <Button
                type="primary"
                key="primary"
                onClick={() => {
                    this.handleCreateContestVisiale(true);
                }}
            >
                <PlusOutlined />
                发布考试
            </Button>,
        ]
    }

    render() {
        return (
            <PageContainer

            >
                <ProCard>
                    <ProTable
                        headerTitle={'考试列表'}
                        columns={this.columns}
                        toolBarRender={() => this.renderToolBar()}
                        request={(params, sort, filter) => this.listEContest(params, sort, filter)}
                    >
                    </ProTable>
                    <ModalForm
                        title={'发布考试'}
                        width="400px"
                        visible={this.state.CreateContestVisiale}
                        onVisibleChange={v => this.handleCreateContestVisiale(v)}
                        onFinish={async (values) => {
                            const success = await this.handleAddContest(values);
                            if (success) {
                                this.handleCreateContestVisiale(false)
                            }
                        }}
                    >
                        <ProFormText
                            rules={
                                [{
                                    required: true,
                                    message: '标题为必填项'
                                }]
                            }
                            width="md"
                            name="tile"
                            label="考试标题"
                        >
                        </ProFormText>
                        <ProFormSelect
                            name="examPaperId"
                            label="试卷标题"
                            request={async () => [
                                { label: '全部', value: 'all' },
                                { label: '未解决', value: 'open' },
                                { label: '已解决', value: 'closed' },
                                { label: '解决中', value: 'processing' },
                            ]}
                            placeholder="Please select a country"
                            rules={[{ required: true, message: 'Please select your country!' }]}
                        />
                        <ProForm.Group >
                            <ProFormDatePicker name="beginDate" label="开始日期" />
                            <ProFormTimePicker name="beginTime" label="开始时间" />
                        </ProForm.Group>
                        <ProForm.Group>
                            <ProFormDatePicker name="finishDate" label="结束日期" />
                            <ProFormTimePicker name="finishTime" label="结束时间" />
                        </ProForm.Group>
                    </ModalForm>
                </ProCard>
            </PageContainer>
        )
    }
}

export default ContestList;