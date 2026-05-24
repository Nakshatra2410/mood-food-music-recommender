// src/components/MusicCard.jsx
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Button,
  IconButton,
  Tooltip
} from '@mui/material';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';

const MusicCard = ({ music }) => {
  const openSpotify = () => {
    window.open(music.spotify_url, '_blank');
  };

  return (
    <Card 
      sx={{ 
        height: '100%',
        transition: 'transform 0.2s',
        '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 }
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box display="flex" alignItems="center">
            <MusicNoteIcon color="secondary" sx={{ mr: 1, fontSize: 30 }} />
            <Box>
              <Typography variant="h6" noWrap>
                {music.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {music.artist}
              </Typography>
            </Box>
          </Box>
          <Tooltip title="Listen on Spotify">
            <IconButton onClick={openSpotify} color="success">
              <AudiotrackIcon />
            </IconButton>
          </Tooltip>
        </Box>
        
        <Box display="flex" gap={1} mt={2}>
          <Chip label={music.genre} size="small" variant="outlined" />
          <Chip label={music.year} size="small" variant="outlined" />
        </Box>
        
        <Button
          variant="outlined"
          size="small"
          fullWidth
          sx={{ mt: 2 }}
          onClick={openSpotify}
          endIcon={<OpenInNewIcon />}
        >
          Play on Spotify
        </Button>
      </CardContent>
    </Card>
  );
};

export default MusicCard;