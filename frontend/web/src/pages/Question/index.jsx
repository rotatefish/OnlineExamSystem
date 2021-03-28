import { PageContainer } from '@ant-design/pro-layout';
import React, { useState, useEffect } from 'react';
import { Button, Spin } from 'antd';
import styles from './index.less';
import { Link, useIntl } from 'umi';


export default () => {
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 3000);
  }, []);

  const { formatMessage } = useIntl();
  return (
    <PageContainer content="这是一个新页面，从这里进行开发！" className={styles.main}>
      <div>
        <Button>
          {formatMessage({ id: 'menu.home' })}
        </Button>
      </div>
    </PageContainer>
  );
};
