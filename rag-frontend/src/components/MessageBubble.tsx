import React from 'react';
import {
  Box,
  Typography,
  Avatar,
  Paper,
  Chip,
} from '@mui/material';
import {
  SmartToy as AIIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  isLoading?: boolean;
}

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const isAssistant = message.sender === 'assistant';

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        alignItems: 'flex-start',
        gap: 1,
        marginBottom: 1,
      }}
    >
      {!isUser && (
        <Avatar
          sx={{
            backgroundColor: 'primary.main',
            width: 32,
            height: 32,
            marginTop: 0.5,
          }}
        >
          <AIIcon fontSize="small" />
        </Avatar>
      )}

      <Box
        sx={{
          maxWidth: '70%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: isUser ? 'flex-end' : 'flex-start',
        }}
      >
        <Paper
          elevation={1}
          sx={{
            padding: 2,
            backgroundColor: isUser ? 'primary.main' : 'grey.100',
            color: isUser ? 'white' : 'text.primary',
            borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
            border: isUser ? 'none' : '1px solid',
            borderColor: 'grey.200',
            wordBreak: 'break-word',
          }}
        >
          <Typography
            variant="body1"
            sx={{
              lineHeight: 1.5,
              whiteSpace: 'pre-wrap',
              '& a': {
                color: isUser ? 'white' : 'primary.main',
                textDecoration: 'underline',
              },
            }}
          >
            {message.content}
          </Typography>
        </Paper>

        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            marginTop: 0.5,
            marginX: 1,
          }}
        >
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ fontSize: '0.75rem' }}
          >
            {format(message.timestamp, 'HH:mm')}
          </Typography>
          
          {isAssistant && (
            <Chip
              label="RAG"
              size="small"
              variant="outlined"
              sx={{
                height: 16,
                fontSize: '0.65rem',
                borderColor: 'primary.main',
                color: 'primary.main',
              }}
            />
          )}
        </Box>
      </Box>

      {isUser && (
        <Avatar
          sx={{
            backgroundColor: 'secondary.main',
            width: 32,
            height: 32,
            marginTop: 0.5,
          }}
        >
          <PersonIcon fontSize="small" />
        </Avatar>
      )}
    </Box>
  );
};

export default MessageBubble;
