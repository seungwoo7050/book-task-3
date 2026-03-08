import React from 'react';
import { SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { FlashList } from '@shopify/flash-list';
import { chatSchemaSummary } from './storageSchema';
import { createPendingMessage, updateTypingState } from './chatModel';

const messages = [
  createPendingMessage('general', 'client-1', 'Offline hello'),
  { clientId: 'client-2', serverId: 'srv-2', conversationId: 'general', text: 'Acked reply', status: 'sent' as const },
];
const typingState = updateTypingState({}, 'alice', true);
const schemaLabel = chatSchemaSummary.tableNames.join(', ');

export function RealtimeChatStudyApp(): React.JSX.Element {
  return (
    <SafeAreaView style={styles.screen}>
      <Text style={styles.eyebrow}>Chat Product Systems</Text>
      <Text style={styles.title}>Realtime Chat</Text>
      <Text style={styles.subtitle}>
        pending send, ack reconcile, replay, typing/presence를 local-first message model로 설명합니다.
      </Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Conversation List</Text>
        <Text style={styles.cardBody}>typing users: {Object.keys(typingState).length}</Text>
        <Text style={styles.cardBody}>
          schema tables: {chatSchemaSummary.tableNames.length} ({schemaLabel})
        </Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Chat Room</Text>
        <FlashList
          data={messages}
          renderItem={({ item }) => (
            <View style={styles.messageRow}>
              <Text style={styles.messageText}>{item.text}</Text>
              <Text style={styles.messageMeta}>{item.status}</Text>
            </View>
          )}
          keyExtractor={item => item.clientId}
          getItemType={() => 'message'}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f3efe8',
    gap: 12,
    padding: 20,
  },
  eyebrow: {
    color: '#765844',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    color: '#20150f',
    fontSize: 28,
    fontWeight: '800',
  },
  subtitle: {
    color: '#5d4d41',
    fontSize: 15,
    lineHeight: 21,
  },
  card: {
    backgroundColor: '#fffdf8',
    borderColor: '#e8d8ca',
    borderRadius: 20,
    borderWidth: 1,
    gap: 8,
    padding: 16,
  },
  cardTitle: {
    color: '#20150f',
    fontSize: 20,
    fontWeight: '800',
  },
  cardBody: {
    color: '#5a473c',
    fontSize: 14,
  },
  messageRow: {
    borderBottomColor: '#eadfd2',
    borderBottomWidth: 1,
    gap: 2,
    paddingVertical: 8,
  },
  messageText: {
    color: '#241811',
    fontSize: 15,
  },
  messageMeta: {
    color: '#7a685a',
    fontSize: 12,
  },
});
