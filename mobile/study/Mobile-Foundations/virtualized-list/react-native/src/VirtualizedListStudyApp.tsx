import React, { useState } from 'react';
import {
  FlatList,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { FlashList } from '@shopify/flash-list';
import { SAMPLE_BENCHMARK, computeBenchmarkSummary } from './benchmark';
import { createDeterministicItems, itemHeightForType, type StudyListItem } from './listData';
import {
  createPaginationState,
  isPaginationComplete,
  loadNextPage,
} from './pagination';

type ScreenMode = 'flat' | 'flash' | 'summary';

const TOTAL_ITEMS = 10000;
const PAGE_SIZE = 50;
const ITEMS = createDeterministicItems(24, TOTAL_ITEMS);
const SUMMARY = computeBenchmarkSummary(
  SAMPLE_BENCHMARK.flatList,
  SAMPLE_BENCHMARK.flashList,
);

function Chip({
  active,
  label,
  onPress,
}: {
  active: boolean;
  label: string;
  onPress: () => void;
}): React.JSX.Element {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={[styles.chip, active && styles.chipActive]}>
      <Text style={[styles.chipLabel, active && styles.chipLabelActive]}>
        {label}
      </Text>
    </Pressable>
  );
}

function ListCell({ item }: { item: StudyListItem }): React.JSX.Element {
  return (
    <View style={[styles.cell, { minHeight: itemHeightForType(item.type) }]}>
      <Text style={styles.typeBadge}>{item.type.toUpperCase()}</Text>
      <Text style={styles.cellTitle}>{item.title}</Text>
      <Text style={styles.cellSubtitle}>{item.subtitle}</Text>
      <Text style={styles.tagLine}>{item.tags.join(' · ')}</Text>
    </View>
  );
}

function Footer({
  complete,
  onPress,
}: {
  complete: boolean;
  onPress: () => void;
}): React.JSX.Element {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={[styles.footerButton, complete && styles.footerDisabled]}>
      <Text style={styles.footerLabel}>
        {complete ? '모든 항목을 불러왔습니다' : '다음 50개 항목 불러오기'}
      </Text>
    </Pressable>
  );
}

export function VirtualizedListStudyApp(): React.JSX.Element {
  const [mode, setMode] = useState<ScreenMode>('flat');
  const [pagination, setPagination] = useState(
    createPaginationState(TOTAL_ITEMS, PAGE_SIZE),
  );
  const visibleItems = ITEMS.slice(0, pagination.cursor);
  const complete = isPaginationComplete(pagination);

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.header}>
        <Text style={styles.eyebrow}>Mobile Foundations</Text>
        <Text style={styles.title}>Virtualized List Performance</Text>
        <Text style={styles.subtitle}>
          같은 10k dataset을 FlatList baseline과 FlashList v2 optimized path로 비교합니다.
        </Text>
      </View>

      <View style={styles.row}>
        <Chip active={mode === 'flat'} label="FlatList" onPress={() => setMode('flat')} />
        <Chip active={mode === 'flash'} label="FlashList v2" onPress={() => setMode('flash')} />
        <Chip active={mode === 'summary'} label="Benchmark" onPress={() => setMode('summary')} />
      </View>

      {mode === 'summary' ? (
        <View style={styles.summaryCard}>
          <Text style={styles.summaryHeading}>Benchmark Summary</Text>
          <Text style={styles.summaryText}>FPS gain: +{SUMMARY.fpsGain}</Text>
          <Text style={styles.summaryText}>
            Initial render gain: {SUMMARY.renderGainMs}ms
          </Text>
          <Text style={styles.summaryText}>
            Blank-area gain: {SUMMARY.blankAreaGainMs}ms
          </Text>
          <Text style={styles.summaryText}>Memory gain: {SUMMARY.memoryGainMb}MB</Text>
          <Text style={styles.summaryText}>Mount savings: {SUMMARY.mountSavings}</Text>
        </View>
      ) : mode === 'flat' ? (
        <FlatList
          data={visibleItems}
          renderItem={({ item }) => <ListCell item={item} />}
          keyExtractor={item => item.id}
          ListFooterComponent={
            <Footer
              complete={complete}
              onPress={() =>
                !complete && setPagination(previous => loadNextPage(previous))
              }
            />
          }
        />
      ) : (
        <FlashList
          data={visibleItems}
          renderItem={({ item }) => <ListCell item={item} />}
          keyExtractor={item => item.id}
          getItemType={item => item.type}
          ListFooterComponent={
            <Footer
              complete={complete}
              onPress={() =>
                !complete && setPagination(previous => loadNextPage(previous))
              }
            />
          }
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f3efe8',
    paddingHorizontal: 16,
  },
  header: {
    gap: 6,
    paddingVertical: 20,
  },
  eyebrow: {
    color: '#6b4d3a',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    color: '#1d140f',
    fontSize: 28,
    fontWeight: '800',
  },
  subtitle: {
    color: '#5d5147',
    fontSize: 15,
    lineHeight: 21,
  },
  row: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 12,
  },
  chip: {
    borderColor: '#cab8a6',
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  chipActive: {
    backgroundColor: '#1d140f',
    borderColor: '#1d140f',
  },
  chipLabel: {
    color: '#4b3c2f',
    fontWeight: '700',
  },
  chipLabelActive: {
    color: '#f8f4ef',
  },
  cell: {
    backgroundColor: '#fffdf8',
    borderColor: '#eadbcf',
    borderRadius: 18,
    borderWidth: 1,
    gap: 6,
    marginBottom: 12,
    padding: 16,
  },
  typeBadge: {
    color: '#9b5a2d',
    fontSize: 11,
    fontWeight: '800',
  },
  cellTitle: {
    color: '#201611',
    fontSize: 18,
    fontWeight: '700',
  },
  cellSubtitle: {
    color: '#5a4b3f',
    fontSize: 14,
  },
  tagLine: {
    color: '#7f6f61',
    fontSize: 12,
  },
  footerButton: {
    backgroundColor: '#1d140f',
    borderRadius: 18,
    marginBottom: 24,
    padding: 16,
  },
  footerDisabled: {
    backgroundColor: '#8a7769',
  },
  footerLabel: {
    color: '#f8f4ef',
    fontSize: 14,
    fontWeight: '700',
    textAlign: 'center',
  },
  summaryCard: {
    backgroundColor: '#fffdf8',
    borderColor: '#eadbcf',
    borderRadius: 24,
    borderWidth: 1,
    gap: 10,
    padding: 20,
  },
  summaryHeading: {
    color: '#1d140f',
    fontSize: 24,
    fontWeight: '800',
  },
  summaryText: {
    color: '#473a31',
    fontSize: 15,
  },
});
