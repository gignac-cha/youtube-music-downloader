import { PauseIcon, PlayIcon } from '@radix-ui/react-icons';
import { Flex, IconButton, Slider, Text } from '@radix-ui/themes';
import { useCallback, useEffect, useRef, useState } from 'react';
import { messages } from '../../constants/messages';

interface AudioPlayerProps {
  src: string;
  title: string;
  compact?: boolean;
}

const formatTime = (seconds: number): string => {
  if (!isFinite(seconds) || isNaN(seconds)) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

export const AudioPlayer = ({ src, title, compact = true }: AudioPlayerProps) => {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = new Audio(src);
    audio.preload = 'metadata';
    audioRef.current = audio;

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleLoadedMetadata = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('ended', handleEnded);
      audio.pause();
      audio.src = '';
    };
  }, [src]);

  const toggle = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      audio.play();
      setIsPlaying(true);
    }
  }, [isPlaying]);

  const handleSeek = useCallback((value: number[]) => {
    const audio = audioRef.current;
    if (!audio || !value[0]) return;
    audio.currentTime = value[0];
    setCurrentTime(value[0]);
  }, []);

  if (compact) {
    return (
      <IconButton
        size={'1'}
        radius="full"
        onClick={toggle}
        aria-label={
          isPlaying
            ? messages.audio.pauseLabel(title)
            : messages.audio.playLabel(title)
        }
      >
        {isPlaying ? <PauseIcon /> : <PlayIcon />}
      </IconButton>
    );
  }

  return (
    <Flex direction="row" gap="2" align="center" style={{ minWidth: 200 }}>
      <IconButton
        size="1"
        radius="full"
        onClick={toggle}
        aria-label={
          isPlaying
            ? messages.audio.pauseLabel(title)
            : messages.audio.playLabel(title)
        }
      >
        {isPlaying ? <PauseIcon /> : <PlayIcon />}
      </IconButton>
      <Text size="1" color="gray" style={{ minWidth: 35, textAlign: 'right' }}>
        {formatTime(currentTime)}
      </Text>
      <Flex flexGrow="1">
        <Slider
          size="1"
          value={[currentTime]}
          max={duration || 100}
          step={0.1}
          onValueChange={handleSeek}
          aria-label="Seek audio"
        />
      </Flex>
      <Text size="1" color="gray" style={{ minWidth: 35 }}>
        {formatTime(duration)}
      </Text>
    </Flex>
  );
};
