import ProCard from '@ant-design/pro-card';
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
import { Button } from 'antd';

class CreateExamPaper extends PureComponent {


    render() {
        return (
            <PageContainer>
                <ProCard
                    style={{
                        padding: 100,
                    }}
                >
                    <ProForm>
                        <ProFormText
                            label="试卷标题"
                            name="title"
                        >

                        </ProFormText>

                        <ProFormList
                            name="questionList"
                            label="题目列表"
                            rules={[{ required: true }]}
                            creatorButtonProps={{
                                creatorButtonText: '增加题目'
                            }}
                        >
                        
                        </ProFormList>
                        <br></br>
                    </ProForm>
                </ProCard>
            </PageContainer>
        )
    }
}

export default CreateExamPaper;
