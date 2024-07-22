<script lang="ts">
	import { onMount, createEventDispatcher, getContext } from 'svelte';
	const dispatch = createEventDispatcher();
	const i18n = getContext('i18n');

	import XMark from '$lib/components/icons/XMark.svelte';
	import AdvancedParams from '../Settings/Advanced/AdvancedParams.svelte';
	import Valves from '$lib/components/common/Valves.svelte';
	import FileItem from '$lib/components/common/FileItem.svelte';
	import { prompts, settings } from '$lib/stores';
	import { toast } from 'svelte-sonner';
	import { updateUserSettings } from '$lib/apis/users';

	import { user } from '$lib/stores';

	export let models = [];

	export let chatFiles = [];
	export let valves = {};
	export let params = {
		system: ''
	};
	onMount(async () => {
		if ($settings.system) {
			params.system = $settings.system;
		} else if ($prompts.length >= 1) {
			params.system = $prompts[0].content;
		}
	});

	const saveSystemDefaultPrompt= async () => {
		if (params.system.length === 0) {
			toast.error($i18n.t('Choose a prompt before saving...'));
			return;
		}
		settings.set({ ...$settings, system: params.system });
		await updateUserSettings(localStorage.token, { ui: $settings });

		toast.success($i18n.t('Default prompt updated'));
	};
</script>

<div class=" dark:text-white">
	<div class=" flex justify-between dark:text-gray-100 mb-2">
		<div class=" text-lg font-medium self-center font-primary">{$i18n.t('Chat Controls')}</div>
		<button
			class="self-center"
			on:click={() => {
				dispatch('close');
			}}
		>
			<XMark className="size-4" />
		</button>
	</div>

	<div class=" dark:text-gray-200 text-sm font-primary">
		{#if chatFiles.length > 0}
			<div>
				<div class="mb-1.5 font-medium">{$i18n.t('Files')}</div>

				<div class="flex flex-col gap-1">
					{#each chatFiles as file, fileIdx}
						<FileItem
							className="w-full"
							url={`${file?.url}`}
							name={file.name}
							type={file.type}
							dismissible={true}
							on:dismiss={() => {
								// Remove the file from the chatFiles array

								chatFiles.splice(fileIdx, 1);
								chatFiles = chatFiles;
							}}
						/>
					{/each}
				</div>
			</div>

			<hr class="my-2 border-gray-100 dark:border-gray-800" />
		{/if}

		{#if models.length === 1 && models[0]?.pipe?.valves_spec}
			<div>
				<div class=" font-medium">{$i18n.t('Valves')}</div>

				<div>
					<Valves valvesSpec={models[0]?.pipe?.valves_spec} bind:valves />
				</div>
			</div>

			<hr class="my-2 border-gray-100 dark:border-gray-800" />
		{/if}

		<div>
			<!-- <div class="mb-1.5 font-medium">{$i18n.t('System Prompt')} -->
			<!-- </div> -->
			<select
				class="w-full rounded-lg py-2 px-4 text-sm bg-gray-50 dark:text-gray-300 dark:bg-gray-850 outline-none"
				bind:value={params.system}
				placeholder="Select a prompt"
			>
				<option value="" selected disabled>{$i18n.t('Select session role')}</option>
				{#each $prompts as prompt}
					<option value={prompt.content} class="bg-gray-100 dark:bg-gray-700">{prompt.title}</option>
				{/each}
			</select>
			<div>
				<textarea
					bind:value={params.system}
					class="w-full rounded-lg px-4 py-3 text-sm dark:text-gray-300 dark:bg-gray-850 border border-gray-100 dark:border-gray-800 outline-none resize-none"
					rows="3"
					placeholder={$i18n.t('Enter system prompt')}
				/>
			</div>
			<button
				class="self-center mt-0.5 ml-1 text-[0.7rem] text-gray-500 font-primary"
				on:click={saveSystemDefaultPrompt}
			>
				{$i18n.t('Set as default')}
			</button>
		</div>

		<hr class="my-2 border-gray-100 dark:border-gray-800" />

		{#if $user.role === 'admin'}
			<div>
				<div class="mb-1.5 font-medium">{$i18n.t('Advanced Params')}</div>

				<div>
					<AdvancedParams bind:params />
				</div>
			</div>
		{/if}
	</div>
</div>
