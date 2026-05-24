// src/components/FoodCard.jsx
import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
  IconButton,
  Tooltip
} from '@mui/material';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import GoogleIcon from '@mui/icons-material/Google';
import YouTubeIcon from '@mui/icons-material/YouTube';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import CloseIcon from '@mui/icons-material/Close';
import { getRecipeDetails } from '../services/api';

const FoodCard = ({ food }) => {
  const [open, setOpen] = useState(false);
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);

  // Generate Google search URL for recipe
  const googleSearchUrl = `https://www.google.com/search?q=${encodeURIComponent(food.name + ' recipe')}`;
  
  // Generate YouTube search URL for cooking video
  const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(food.name + ' recipe cooking')}`;

  const handleClickOpen = async () => {
    setOpen(true);
    setLoading(true);
    try {
      const details = await getRecipeDetails(food.name);
      setRecipe(details);
    } catch (error) {
      console.error('Error fetching recipe:', error);
    }
    setLoading(false);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy': return '#4caf50';
      case 'medium': return '#ff9800';
      case 'hard': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  const openGoogleSearch = () => {
    window.open(googleSearchUrl, '_blank');
  };

  const openYouTubeSearch = () => {
    window.open(youtubeSearchUrl, '_blank');
  };

  return (
    <>
      <Card 
        sx={{ 
          height: '100%', 
          cursor: 'pointer',
          transition: 'transform 0.2s',
          '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
          borderRadius: 2,
        }}
        onClick={handleClickOpen}
      >
        <CardContent>
          <Box display="flex" alignItems="center" mb={1}>
            <RestaurantIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6" noWrap>
              {food.name}
            </Typography>
          </Box>
          
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {food.cuisine} • {food.type}
          </Typography>
          
          <Box display="flex" alignItems="center" gap={1} mt={1}>
            <Chip 
              icon={<AccessTimeIcon />} 
              label={food.prep_time} 
              size="small" 
              variant="outlined"
            />
            <Chip 
              icon={<WhatshotIcon />} 
              label={food.difficulty} 
              size="small" 
              sx={{ 
                color: getDifficultyColor(food.difficulty),
                borderColor: getDifficultyColor(food.difficulty),
              }}
            />
            {food.calories && (
              <Chip 
                label={`${food.calories} cal`} 
                size="small" 
                variant="outlined"
              />
            )}
          </Box>
        </CardContent>
      </Card>

      {/* Styled Dialog with Icons */}
      <Dialog 
        open={open} 
        onClose={handleClose} 
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 3,
          }
        }}
      >
        <DialogTitle sx={{ 
          background: `linear-gradient(135deg, ${getDifficultyColor(food.difficulty)} 0%, ${getDifficultyColor(food.difficulty)}cc 100%)`,
          color: 'white',
          position: 'relative',
          pb: 2
        }}>
          <IconButton
            onClick={handleClose}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
              color: 'white',
            }}
          >
            <CloseIcon />
          </IconButton>
          <Box display="flex" alignItems="center" gap={2}>
            <RestaurantIcon sx={{ fontSize: 40 }} />
            <Box>
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {food.name}
              </Typography>
              <Typography variant="subtitle2">
                {food.cuisine} • {food.type}
              </Typography>
            </Box>
          </Box>
        </DialogTitle>
        
        <DialogContent dividers>
          {loading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : recipe ? (
            <>
              {/* Quick Info */}
              <Box display="flex" gap={2} mb={3} flexWrap="wrap">
                <Chip icon={<AccessTimeIcon />} label={`${food.prep_time}`} />
                <Chip icon={<WhatshotIcon />} label={`${food.difficulty}`} />
                {food.calories && <Chip label={`📊 ${food.calories} cal`} />}
              </Box>

              {/* Ingredients */}
              <Typography variant="h6" gutterBottom>📝 Ingredients</Typography>
              <List dense>
                {(recipe.ingredients || food.ingredients || ['Ingredients not available']).map((ing, idx) => (
                  <ListItem key={idx}>
                    <ListItemText primary={ing} />
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              {/* Instructions */}
              <Typography variant="h6" gutterBottom>👨‍🍳 Instructions</Typography>
              <Typography variant="body2" paragraph>
                {recipe.instructions || `Step by step instructions for ${food.name}.\n\nCombine all ingredients and cook with care and love!`}
              </Typography>

              {/* Google & YouTube Icons Section */}
              <Box display="flex" gap={2} justifyContent="center" mt={3}>
                <Button
                  variant="contained"
                  startIcon={<GoogleIcon />}
                  onClick={openGoogleSearch}
                  sx={{ 
                    bgcolor: '#4285f4', 
                    '&:hover': { bgcolor: '#3367d6' },
                    borderRadius: 2,
                    textTransform: 'none',
                    px: 3
                  }}
                >
                  Search on Google
                </Button>
                <Button
                  variant="contained"
                  startIcon={<YouTubeIcon />}
                  onClick={openYouTubeSearch}
                  sx={{ 
                    bgcolor: '#ff0000', 
                    '&:hover': { bgcolor: '#cc0000' },
                    borderRadius: 2,
                    textTransform: 'none',
                    px: 3
                  }}
                >
                  Watch on YouTube
                </Button>
              </Box>
            </>
          ) : (
            <Box sx={{ textAlign: 'center', py: 3 }}>
              <Typography variant="body1" gutterBottom>
                Want to make {food.name}?
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Find recipes and cooking videos online!
              </Typography>
              <Box display="flex" gap={2} justifyContent="center">
                <Button
                  variant="contained"
                  startIcon={<GoogleIcon />}
                  onClick={openGoogleSearch}
                  sx={{ 
                    bgcolor: '#4285f4', 
                    '&:hover': { bgcolor: '#3367d6' },
                    borderRadius: 2,
                    textTransform: 'none',
                  }}
                >
                  Google Recipe
                </Button>
                <Button
                  variant="contained"
                  startIcon={<YouTubeIcon />}
                  onClick={openYouTubeSearch}
                  sx={{ 
                    bgcolor: '#ff0000', 
                    '&:hover': { bgcolor: '#cc0000' },
                    borderRadius: 2,
                    textTransform: 'none',
                  }}
                >
                  YouTube Video
                </Button>
              </Box>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
          <Button 
            variant="outlined" 
            startIcon={<OpenInNewIcon />}
            onClick={openGoogleSearch}
          >
            Find Recipes Online
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default FoodCard;