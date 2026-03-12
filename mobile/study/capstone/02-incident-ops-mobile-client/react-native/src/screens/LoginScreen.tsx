import React, { useEffect, useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { StyleSheet, Text, View } from 'react-native';

import { useAppModel } from '../app/AppModel';
import { ActionButton, AppTextField, ScreenLayout, SectionCard, sharedStyles } from '../components/Ui';
import { loginSchema, type LoginFormValues } from '../lib/forms';
import { USER_ROLES } from '../contracts';
import { theme } from '../theme';

export function LoginScreen() {
  const { login, settings } = useAppModel();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
    watch,
    reset,
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      userId: '',
      role: 'REPORTER',
      baseUrl: settings.baseUrl,
    },
  });

  const selectedRole = watch('role');

  useEffect(() => {
    reset({
      userId: '',
      role: 'REPORTER',
      baseUrl: settings.baseUrl,
    });
  }, [reset, settings.baseUrl]);

  const submit = handleSubmit(async values => {
    setSubmitError(null);
    try {
      await login(values);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'login failed');
    }
  });

  return (
    <ScreenLayout scroll>
      <SectionCard eyebrow="Final Capstone" title="Incident Ops Client">
        <Text style={styles.lead}>
          역할 기반 승인 흐름, persistent outbox, replay-safe realtime 계약을
          하나의 RN 완성작으로 묶는 로그인 진입점입니다.
        </Text>
      </SectionCard>

      <SectionCard title="Auth Stack">
        <Controller
          control={control}
          name="userId"
          render={({ field: { onChange, value } }) => (
            <AppTextField
              autoCapitalize="none"
              errorText={errors.userId?.message}
              label="User ID"
              onChangeText={onChange}
              placeholder="reporter.demo"
              testID="login-user-id-input"
              value={value}
            />
          )}
        />

        <Controller
          control={control}
          name="baseUrl"
          render={({ field: { onChange, value } }) => (
            <AppTextField
              autoCapitalize="none"
              errorText={errors.baseUrl?.message}
              label="Base URL"
              onChangeText={onChange}
              placeholder="http://127.0.0.1:4100"
              testID="login-base-url-input"
              value={value}
            />
          )}
        />

        <View style={sharedStyles.rowWrap}>
          {USER_ROLES.map(role => (
            <ActionButton
              disabled={isSubmitting}
              key={role}
              label={role}
              onPress={() => {
                setValue('role', role, { shouldValidate: true });
              }}
              tone={selectedRole === role ? 'solid' : 'ghost'}
            />
          ))}
        </View>

        {submitError ? <Text style={styles.error}>{submitError}</Text> : null}

        <ActionButton
          disabled={isSubmitting}
          label={isSubmitting ? 'Signing In...' : 'Continue'}
          onPress={submit}
          testID="login-submit-button"
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
  error: {
    color: theme.color.danger,
    fontSize: 14,
  },
});
