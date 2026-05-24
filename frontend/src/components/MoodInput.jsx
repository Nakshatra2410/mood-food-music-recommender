// src/components/MoodInput.jsx
import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Box,
  CircularProgress,
  Typography
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const MoodInput = ({ onAnalyze, loading }) => {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim()) {
      onAnalyze(text);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
      <Typography variant="h5" gutterBottom>
        How are you feeling today?
      </Typography>
      <TextField
        fullWidth
        multiline
        rows={3}
        variant="outlined"
        placeholder="e.g., I'm feeling really happy and excited about my promotion!"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={loading}
        sx={{ mb: 2 }}
      />
      <Button
        variant="contained"
        size="large"
        onClick={handleSubmit}
        disabled={loading || !text.trim()}
        startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
      >
        {loading ? 'Analyzing your mood...' : 'Get Recommendations'}
      </Button>
    </Paper>
  );
};

export default MoodInput;