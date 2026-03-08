import React, { useState } from 'react';
import {
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  Vibration,
  View,
} from 'react-native';
import {
  Gesture,
  GestureDetector,
  GestureHandlerRootView,
} from 'react-native-gesture-handler';
import Animated, {
  interpolate,
  useAnimatedStyle,
  useSharedValue,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {
  getDismissProgress,
  getSwipeDecision,
  reorderByOffset,
} from './gestureMath';

const Stack = createNativeStackNavigator();
const SWIPE_THRESHOLD = 120;
const ROW_HEIGHT = 58;

function SwipeCardDemo(): React.JSX.Element {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);

  const pan = Gesture.Pan()
    .onUpdate(event => {
      translateX.value = event.translationX;
      translateY.value = event.translationY * 0.35;
    })
    .onEnd(() => {
      const decision = getSwipeDecision(translateX.value, SWIPE_THRESHOLD);
      if (decision === 'reset') {
        translateX.value = withSpring(0, { damping: 16, stiffness: 190 });
        translateY.value = withSpring(0, { damping: 16, stiffness: 190 });
        return;
      }

      translateX.value = withTiming(
        decision === 'like' ? 360 : -360,
        { duration: 220 },
        finished => {
          if (finished) {
            translateX.value = 0;
            translateY.value = 0;
          }
        },
      );
    });

  const style = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
      { rotate: `${translateX.value / 12}deg` },
    ],
  }));

  const likeStyle = useAnimatedStyle(() => ({
    opacity: interpolate(translateX.value, [0, SWIPE_THRESHOLD], [0, 1]),
  }));

  const nopeStyle = useAnimatedStyle(() => ({
    opacity: interpolate(translateX.value, [-SWIPE_THRESHOLD, 0], [1, 0]),
  }));

  return (
    <View style={styles.panel}>
      <Text style={styles.panelTitle}>Swipe Card</Text>
      <GestureDetector gesture={pan}>
        <Animated.View style={[styles.card, style]}>
          <Animated.Text style={[styles.badgeLeft, nopeStyle]}>NOPE</Animated.Text>
          <Animated.Text style={[styles.badgeRight, likeStyle]}>LIKE</Animated.Text>
          <Text style={styles.cardName}>Taylor Park</Text>
          <Text style={styles.cardMeta}>drag horizontally to dismiss</Text>
        </Animated.View>
      </GestureDetector>
    </View>
  );
}

function ReorderDemo(): React.JSX.Element {
  const [items, setItems] = useState(['Signal', 'Latency', 'Outbox', 'Replay']);

  return (
    <View style={styles.panel}>
      <Text style={styles.panelTitle}>Reorder List</Text>
      {items.map((item, index) => (
        <Pressable
          key={item}
          accessibilityRole="button"
          onPress={() => {
            Vibration.vibrate(10);
            setItems(previous => reorderByOffset(previous, index, ROW_HEIGHT, ROW_HEIGHT));
          }}
          style={styles.rowItem}>
          <Text style={styles.rowLabel}>{item}</Text>
          <Text style={styles.rowMeta}>tap to simulate one-row drag</Text>
        </Pressable>
      ))}
    </View>
  );
}

function SharedGalleryScreen({
  navigation,
}: {
  navigation: { navigate: (name: string, params?: { title?: string }) => void };
}): React.JSX.Element {
  return (
    <SafeAreaView style={styles.screen}>
      <SwipeCardDemo />
      <ReorderDemo />
      <Pressable
        accessibilityRole="button"
        onPress={() => navigation.navigate('Detail', { title: 'Shared Transition' })}
        style={styles.galleryCard}>
        <Animated.View sharedTransitionTag="gesture-photo" style={styles.photoBlock} />
        <Text style={styles.galleryTitle}>Shared Transition Detail</Text>
        <Text style={styles.galleryMeta}>open detail and drag down to dismiss</Text>
      </Pressable>
    </SafeAreaView>
  );
}

function SharedDetailScreen({
  navigation,
  route,
}: {
  navigation: { goBack: () => void };
  route: { params?: { title?: string } };
}): React.JSX.Element {
  const translateY = useSharedValue(0);
  const dismiss = Gesture.Pan()
    .onUpdate(event => {
      translateY.value = Math.max(0, event.translationY);
    })
    .onEnd(() => {
      if (getDismissProgress(translateY.value, 160) > 0.6) {
        translateY.value = 0;
        navigation.goBack();
        return;
      }

      translateY.value = withSpring(0, { damping: 18, stiffness: 180 });
    });

  const sheetStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));

  return (
    <GestureDetector gesture={dismiss}>
      <Animated.View style={[styles.detailScreen, sheetStyle]}>
        <Animated.View sharedTransitionTag="gesture-photo" style={styles.photoHero} />
        <Text style={styles.detailTitle}>
          {route.params?.title ?? 'Shared Transition'}
        </Text>
        <Text style={styles.detailMeta}>swipe down to reverse the transition</Text>
      </Animated.View>
    </GestureDetector>
  );
}

export function GesturesStudyApp(): React.JSX.Element {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Home" component={SharedGalleryScreen} />
          <Stack.Screen name="Detail" component={SharedDetailScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#fff8eb',
    gap: 18,
    padding: 18,
  },
  panel: {
    backgroundColor: '#fffef9',
    borderColor: '#eedfc4',
    borderRadius: 24,
    borderWidth: 1,
    gap: 12,
    padding: 18,
  },
  panelTitle: {
    color: '#24160f',
    fontSize: 22,
    fontWeight: '800',
  },
  card: {
    backgroundColor: '#2c2018',
    borderRadius: 22,
    minHeight: 220,
    overflow: 'hidden',
    padding: 18,
  },
  badgeLeft: {
    color: '#ff7c64',
    fontSize: 16,
    fontWeight: '800',
  },
  badgeRight: {
    color: '#96ff9a',
    fontSize: 16,
    fontWeight: '800',
    textAlign: 'right',
  },
  cardName: {
    color: '#fff8eb',
    fontSize: 28,
    fontWeight: '800',
    marginTop: 60,
  },
  cardMeta: {
    color: '#ead3be',
    fontSize: 14,
  },
  rowItem: {
    backgroundColor: '#fff2dc',
    borderRadius: 16,
    minHeight: ROW_HEIGHT,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
  rowLabel: {
    color: '#2a1a12',
    fontSize: 18,
    fontWeight: '700',
  },
  rowMeta: {
    color: '#735948',
    fontSize: 12,
  },
  galleryCard: {
    backgroundColor: '#261814',
    borderRadius: 24,
    overflow: 'hidden',
    paddingBottom: 18,
  },
  photoBlock: {
    backgroundColor: '#ad7f63',
    height: 170,
  },
  galleryTitle: {
    color: '#fff6ea',
    fontSize: 22,
    fontWeight: '800',
    paddingHorizontal: 18,
    paddingTop: 14,
  },
  galleryMeta: {
    color: '#dbc7b8',
    fontSize: 13,
    paddingHorizontal: 18,
  },
  detailScreen: {
    flex: 1,
    backgroundColor: '#1d1210',
    paddingTop: 60,
  },
  photoHero: {
    backgroundColor: '#ad7f63',
    borderRadius: 28,
    height: 280,
    marginHorizontal: 16,
  },
  detailTitle: {
    color: '#fff7ef',
    fontSize: 28,
    fontWeight: '800',
    marginHorizontal: 18,
    marginTop: 18,
  },
  detailMeta: {
    color: '#d7bfb2',
    fontSize: 14,
    marginHorizontal: 18,
    marginTop: 6,
  },
});
