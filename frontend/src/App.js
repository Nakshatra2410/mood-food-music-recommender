// src/App.js
import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Chip,
  LinearProgress,
  Alert,
  Snackbar,
  Tab,
  Tabs,
  AppBar,
  Toolbar,
  Button,
  Avatar,
  Fade,
  Grow,
  Zoom
} from '@mui/material';
import { ThemeProvider, createTheme, alpha } from '@mui/material/styles';
import EmojiEmotionsIcon from '@mui/icons-material/EmojiEmotions';
import RestaurantMenuIcon from '@mui/icons-material/RestaurantMenu';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import HistoryIcon from '@mui/icons-material/History';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import MoodInput from './components/MoodInput';
import FoodCard from './components/FoodCard';
import MusicCard from './components/MusicCard';
import { getRecommendations } from './services/api';

// Beautiful custom theme - ONLY STYLING, NO COMPONENT CHANGES
const theme = createTheme({
  palette: {
    primary: {
      main: '#ff6b6b',
      light: '#ff8e8e',
      dark: '#ff4a4a',
    },
    secondary: {
      main: '#4ecdc4',
      light: '#6ed9d1',
      dark: '#3ab4ab',
    },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
      letterSpacing: '-0.5px',
    },
    h5: {
      fontWeight: 500,
    },
    h6: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 16,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 12,
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
  },
});

function TabPanel({ children, value, index }) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const [history, setHistory] = useState([]);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const handleAnalyze = async (text) => {
    setLoading(true);
    setError('');
    
    try {
      const result = await getRecommendations(text);
      setRecommendation(result);
      
      setHistory(prev => [{
        id: Date.now(),
        text: text,
        mood: result.mood,
        timestamp: new Date()
      }, ...prev].slice(0, 10));
      
      setSnackbarOpen(true);
      setTabValue(0);
    } catch (err) {
      setError('Failed to get recommendations. Please make sure the backend server is running at http://localhost:8000');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getMoodColor = (mood) => {
    const colors = {
      joy: '#FFD700',
      sadness: '#6B8EFF',
      love: '#FF6B6B',
      anger: '#FF4444',
      fear: '#9370DB',
      surprise: '#FFA500'
    };
    return colors[mood] || '#808080';
  };

  const getMoodGradient = (mood) => {
    const gradients = {
      joy: 'linear-gradient(135deg, #FFD700 0%, #FFB347 100%)',
      sadness: 'linear-gradient(135deg, #6B8EFF 0%, #4A6EFF 100%)',
      love: 'linear-gradient(135deg, #FF6B6B 0%, #FF4A4A 100%)',
      anger: 'linear-gradient(135deg, #FF4444 0%, #CC0000 100%)',
      fear: 'linear-gradient(135deg, #9370DB 0%, #6A4E9E 100%)',
      surprise: 'linear-gradient(135deg, #FFA500 0%, #FF6B00 100%)'
    };
    return gradients[mood] || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
  };

  const getMoodEmoji = (mood) => {
    const emojis = {
      joy: '😊',
      sadness: '😢',
      love: '❤️',
      anger: '😠',
      fear: '😨',
      surprise: '😲'
    };
    return emojis[mood] || '😊';
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
      }}>
        {/* Simple decorative background - purely visual */}
        <Box sx={{ 
          position: 'fixed', 
          top: '10%', 
          left: '5%', 
          opacity: 0.05, 
          pointerEvents: 'none',
          fontSize: 120
        }}>
          🎵
        </Box>
        <Box sx={{ 
          position: 'fixed', 
          bottom: '10%', 
          right: '5%', 
          opacity: 0.05, 
          pointerEvents: 'none',
          fontSize: 120
        }}>
          🍔
        </Box>

        <Container maxWidth="lg" sx={{ py: 4, position: 'relative', zIndex: 1 }}>
          {/* Hero Section - Styled but not changing functionality */}
          <Grow in={true} timeout={800}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: 4, 
                mb: 4, 
                textAlign: 'center',
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.3)',
              }}
            >
              <Box display="flex" alignItems="center" justifyContent="center" gap={2} mb={2}>
                <Avatar sx={{ bgcolor: '#ff6b6b', width: 56, height: 56 }}>
                  <AutoAwesomeIcon sx={{ fontSize: 32 }} />
                </Avatar>
                <Typography variant="h3" sx={{ fontWeight: 700 }}>
                  Mood & Flavor
                </Typography>
              </Box>
              <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
                Tell me how you feel, and I'll recommend the perfect food and music
              </Typography>
            </Paper>
          </Grow>

          {/* MoodInput - UNCHANGED, works exactly as before */}
          <MoodInput onAnalyze={handleAnalyze} loading={loading} />

          {error && (
            <Fade in={true}>
              <Alert severity="error" sx={{ mt: 2, borderRadius: 2 }} onClose={() => setError('')}>
                {error}
              </Alert>
            </Fade>
          )}

          {loading && (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <LinearProgress sx={{ borderRadius: 2, height: 8 }} />
              <Typography variant="body2" color="white" sx={{ mt: 1 }}>
                Analyzing your mood...
              </Typography>
            </Box>
          )}

          {recommendation && (
            <Zoom in={true} timeout={500}>
              <Box>
                {/* Mood Card - Styled beautifully, but same functionality */}
                <Paper 
                  sx={{ 
                    mt: 4, 
                    p: 4, 
                    borderRadius: 4,
                    background: getMoodGradient(recommendation.mood),
                    color: 'white',
                    position: 'relative',
                    overflow: 'hidden',
                  }}
                >
                  <Box display="flex" alignItems="center" justifyContent="space-between" flexWrap="wrap">
                    <Box display="flex" alignItems="center" gap={2}>
                      <Typography variant="h1" sx={{ fontSize: 64 }}>
                        {getMoodEmoji(recommendation.mood)}
                      </Typography>
                      <Box>
                        <Typography variant="h4" sx={{ fontWeight: 700 }}>
                          {recommendation.mood.toUpperCase()}
                        </Typography>
                        <Chip 
                          label={`${(recommendation.confidence * 100).toFixed(1)}% confidence`}
                          size="small"
                          sx={{ 
                            mt: 1, 
                            bgcolor: 'rgba(255,255,255,0.2)', 
                            color: 'white',
                            fontWeight: 500
                          }}
                        />
                      </Box>
                    </Box>
                    <Typography variant="body1" sx={{ maxWidth: 400, opacity: 0.95 }}>
                      {recommendation.mood_response}
                    </Typography>
                  </Box>
                </Paper>

                {/* Tabs - Styled but keeping same behavior */}
                <Paper sx={{ mt: 3, borderRadius: 3, overflow: 'hidden' }}>
                  <Tabs 
                    value={tabValue} 
                    onChange={(e, v) => setTabValue(v)}
                    sx={{
                      borderBottom: 1,
                      borderColor: 'divider',
                      '& .MuiTab-root': {
                        textTransform: 'none',
                        fontWeight: 600,
                        fontSize: '1rem',
                        py: 2,
                      }
                    }}
                  >
                    <Tab icon={<RestaurantMenuIcon />} iconPosition="start" label="🍔 Food" />
                    <Tab icon={<MusicNoteIcon />} iconPosition="start" label="🎵 Music" />
                    <Tab label="📊 Analysis" />
                  </Tabs>

                  {/* Food Tab - Uses your existing FoodCard component */}
                  <TabPanel value={tabValue} index={0}>
                    <Grid container spacing={3}>
                      {recommendation.food_recommendations.map((food, idx) => (
                        <Grid item xs={12} md={4} key={idx}>
                          <FoodCard food={food} />
                        </Grid>
                      ))}
                    </Grid>
                  </TabPanel>

                  {/* Music Tab - Uses your existing MusicCard component */}
                  <TabPanel value={tabValue} index={1}>
                    <Grid container spacing={3}>
                      {recommendation.music_recommendations.map((music, idx) => (
                        <Grid item xs={12} md={4} key={idx}>
                          <MusicCard music={music} />
                        </Grid>
                      ))}
                    </Grid>
                  </TabPanel>

                  {/* Analysis Tab */}
                  <TabPanel value={tabValue} index={2}>
                    <Paper elevation={0} sx={{ p: 3, borderRadius: 2 }}>
                      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                        Mood Probability Distribution
                      </Typography>
                      {Object.entries(recommendation.all_mood_scores).map(([mood, score]) => (
                        <Box key={mood} sx={{ mb: 2 }}>
                          <Box display="flex" justifyContent="space-between" mb={1}>
                            <Box display="flex" alignItems="center" gap={1}>
                              <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                                {mood}
                              </Typography>
                              <span>{getMoodEmoji(mood)}</span>
                            </Box>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {(score * 100).toFixed(1)}%
                            </Typography>
                          </Box>
                          <LinearProgress 
                            variant="determinate" 
                            value={score * 100} 
                            sx={{ 
                              height: 10, 
                              borderRadius: 5,
                              bgcolor: alpha(getMoodColor(mood), 0.2),
                              '& .MuiLinearProgress-bar': {
                                bgcolor: getMoodColor(mood),
                                borderRadius: 5,
                              }
                            }}
                          />
                        </Box>
                      ))}
                    </Paper>
                  </TabPanel>
                </Paper>
              </Box>
            </Zoom>
          )}

          {/* History Section - Styled but keeps functionality */}
          {history.length > 0 && (
            <Fade in={true}>
              <Paper elevation={0} sx={{ mt: 4, p: 3, borderRadius: 3, bgcolor: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)' }}>
                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <HistoryIcon color="primary" />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>Recent Moods</Typography>
                </Box>
                <Grid container spacing={2}>
                  {history.map((item) => (
                    <Grid item xs={12} sm={6} md={4} key={item.id}>
                      <Paper 
                        elevation={0} 
                        sx={{ 
                          p: 2, 
                          borderRadius: 2,
                          bgcolor: alpha(getMoodColor(item.mood), 0.1),
                          border: `1px solid ${alpha(getMoodColor(item.mood), 0.3)}`,
                          cursor: 'pointer',
                          transition: 'all 0.2s',
                          '&:hover': {
                            transform: 'translateX(4px)',
                            bgcolor: alpha(getMoodColor(item.mood), 0.15),
                          }
                        }}
                        onClick={() => handleAnalyze(item.text)}
                      >
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="h6">{getMoodEmoji(item.mood)}</Typography>
                          <Box flex={1}>
                            <Typography variant="body2" noWrap sx={{ fontWeight: 500 }}>
                              {item.text}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {item.timestamp.toLocaleTimeString()}
                            </Typography>
                          </Box>
                          <Chip 
                            label={item.mood} 
                            size="small" 
                            sx={{ 
                              bgcolor: getMoodColor(item.mood),
                              color: item.mood === 'joy' ? '#333' : 'white',
                              fontWeight: 500
                            }}
                          />
                        </Box>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Fade>
          )}

          <Snackbar
            open={snackbarOpen}
            autoHideDuration={3000}
            onClose={() => setSnackbarOpen(false)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          >
            <Paper sx={{ p: 2, borderRadius: 3, bgcolor: '#4caf50', color: 'white' }}>
              ✨ Recommendations ready! Enjoy!
            </Paper>
          </Snackbar>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;