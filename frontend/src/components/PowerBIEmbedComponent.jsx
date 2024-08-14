import React, { useEffect, useState } from 'react';
import api from '../api';  // Ensure this is your configured axios instance
import { PowerBIEmbed } from 'powerbi-client-react';
import { models } from 'powerbi-client';

const PowerBIEmbedComponent = ({ userType }) => {
  const [embedConfig, setEmbedConfig] = useState(null);

  useEffect(() => {
    const fetchEmbedConfig = async () => {
      try {
        const response = await api.get(`/KPI/api/get_embed_config/${userType}/`);
        console.log('Embed config:', response.data); // Debugging line
        setEmbedConfig(response.data);
      } catch (error) {
        console.error('Error fetching embed config:', error);
      }
    };

    fetchEmbedConfig();
  }, [userType]);

  if (!embedConfig) {
    return <div>Loading...</div>;
  }

  return (
    <PowerBIEmbed
      embedConfig={{
        type: 'report',
        id: embedConfig.id,
        embedUrl: embedConfig.embedUrl,
        accessToken: embedConfig.accessToken,
        tokenType: models.TokenType.Embed,
        settings: embedConfig.settings,
      }}
      cssClassName="report-style-class"
      eventHandlers={
        new Map([
          ['loaded', async function () {
            console.log('Report loaded');
            const report = window.powerbi.get(this);
            if (embedConfig.pageId) {
              try {
                await report.setPage(embedConfig.pageId);
                console.log(`Navigated to page: ${embedConfig.pageId}`);
              } catch (error) {
                console.error(`Error setting page: ${embedConfig.pageId}`, error);
              }
            }
          }],
        ])
      }
      getEmbeddedComponent={(embeddedReport) => {
        console.log('Embedded report:', embeddedReport);
      }}
      style={{ width: '100%', height: '100%' }} // Ensure full width and height
    />
  );
};

export default PowerBIEmbedComponent;
