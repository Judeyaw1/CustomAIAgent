import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
  IconButton,
} from '@mui/material';
import {
  SmartToy as AIIcon,
  Description as DocumentIcon,
  CheckCircle as StatusIcon,
} from '@mui/icons-material';

const Header: React.FC = () => {
  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{ 
        backgroundColor: 'white',
        borderBottom: '1px solid #e0e0e0',
        color: 'text.primary',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              padding: 1,
              backgroundColor: 'primary.main',
              borderRadius: 2,
              color: 'white',
            }}
          >
            <AIIcon />
            <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
              RAG Assistant
            </Typography>
          </Box>
          
          <Chip
            icon={<DocumentIcon />}
            label="Business Information Systems"
            variant="outlined"
            size="small"
            sx={{ 
              borderColor: 'primary.main',
              color: 'primary.main',
            }}
          />
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Chip
            icon={<StatusIcon />}
            label="Online"
            color="success"
            size="small"
            variant="outlined"
          />
          
          <IconButton size="small" sx={{ color: 'text.secondary' }}>
            <DocumentIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
