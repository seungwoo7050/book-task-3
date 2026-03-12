import React from 'react';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

import { useAppModel } from '../app/AppModel';
import {
  ActionButton,
  AppTextField,
  ScreenLayout,
  SectionCard,
  sharedStyles,
} from '../components/Ui';
import { INCIDENT_SEVERITIES } from '../contracts';
import {
  createIncidentSchema,
  type CreateIncidentFormValues,
} from '../lib/forms';
import { theme } from '../theme';
import type { IncidentStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<IncidentStackParamList, 'CreateIncident'>;

export function CreateIncidentScreen({ navigation }: Props) {
  const { queueCreateIncident } = useAppModel();
  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
    watch,
  } = useForm<CreateIncidentFormValues>({
    resolver: zodResolver(createIncidentSchema),
    defaultValues: {
      title: '',
      description: '',
      severity: 'P2',
    },
  });

  const severity = watch('severity');

  const submit = handleSubmit(values => {
    queueCreateIncident(values);
    navigation.goBack();
  });

  return (
    <ScreenLayout scroll>
      <SectionCard eyebrow="Incident Flow" title="Queue New Incident">
        <Text style={styles.lead}>
          생성 요청은 즉시 outbox job으로 기록되고, 연결 상태에 따라 바로 flush되거나
          pending 상태로 유지됩니다.
        </Text>
      </SectionCard>

      <SectionCard title="Create Form">
        <Controller
          control={control}
          name="title"
          render={({ field: { onChange, value } }) => (
            <AppTextField
              errorText={errors.title?.message}
              label="Title"
              onChangeText={onChange}
              placeholder="Database latency spike"
              testID="create-title-input"
              value={value}
            />
          )}
        />

        <Controller
          control={control}
          name="description"
          render={({ field: { onChange, value } }) => (
            <AppTextField
              errorText={errors.description?.message}
              label="Description"
              multiline
              onChangeText={onChange}
              placeholder="What happened, who is affected, what is the current mitigation?"
              testID="create-description-input"
              value={value}
            />
          )}
        />

        <View style={sharedStyles.rowWrap}>
          {INCIDENT_SEVERITIES.map(level => (
            <ActionButton
              key={level}
              label={level}
              onPress={() => setValue('severity', level, { shouldValidate: true })}
              tone={severity === level ? 'solid' : 'ghost'}
            />
          ))}
        </View>

        <ActionButton
          disabled={isSubmitting}
          label={isSubmitting ? 'Queueing...' : 'Queue Incident'}
          onPress={submit}
          testID="queue-incident-button"
        />
      </SectionCard>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  lead: {
    color: theme.color.mutedInk,
    fontSize: 15,
    lineHeight: 22,
  },
});
