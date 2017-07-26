## 3.15\. Instant Apps

Device implementations MUST satisfy the following requirements:

*   Instant Apps MUST only be granted permissions that have the
    [`android:protectionLevel`](https://developer.android.com/guide/topics/manifest/permission-element.html#plevel)
    set to `"ephemeral"`.
*   Instant Apps MUST NOT interact with installed apps via [implicit intents](https://developer.android.com/reference/android/content/Intent.html)
    unless one of the following is true:
    *   The component's intent pattern filter is exposed and has CATEGORY_BROWSABLE
    *   The action is one of ACTION_SEND, ACTION_SENDTO, ACTION_SEND_MULTIPLE
    *   The target is explicitly exposed with [android:visibleToInstantApps](https://developer.android.com/reference/android/R.attr.html#visibleToInstantApps)
*   Instant Apps MUST NOT interact explicitly with installed apps unless the
    component is exposed via android:visibleToInstantApps.
*   Installed Apps MUST NOT see details about Instant Apps on the
    device unless the Instant App explicitly connects to the
    installed application.