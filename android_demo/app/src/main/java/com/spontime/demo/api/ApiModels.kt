package com.spontime.demo.api

import com.google.gson.annotations.SerializedName

data class User(
    @SerializedName("id") val id: String,
    @SerializedName("handle") val handle: String,
    @SerializedName("display_name") val displayName: String?,
    @SerializedName("email") val email: String?,
    @SerializedName("phone") val phone: String?,
    @SerializedName("photo_url") val photoUrl: String?,
    @SerializedName("language") val language: String,
    @SerializedName("status") val status: String,
    @SerializedName("created_at") val createdAt: String
)

data class RegisterRequest(
    @SerializedName("email") val email: String,
    @SerializedName("handle") val handle: String,
    @SerializedName("password") val password: String,
    @SerializedName("display_name") val displayName: String? = null
)

data class LoginRequest(
    @SerializedName("email") val email: String,
    @SerializedName("password") val password: String
)

data class AuthResponse(
    @SerializedName("token") val token: String,
    @SerializedName("user") val user: User,
    @SerializedName("message") val message: String
)

data class ErrorResponse(
    @SerializedName("error") val error: String? = null,
    @SerializedName("detail") val detail: String? = null
)

data class Plan(
    @SerializedName("id") val id: String,
    @SerializedName("title") val title: String,
    @SerializedName("description") val description: String?,
    @SerializedName("starts_at") val startsAt: String?,
    @SerializedName("ends_at") val endsAt: String?,
    @SerializedName("capacity") val capacity: Int?,
    @SerializedName("visibility") val visibility: String,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("host_user") val hostUser: User?,
    @SerializedName("created_at") val createdAt: String
)

data class PaginatedResponse<T>(
    @SerializedName("count") val count: Int,
    @SerializedName("next") val next: String?,
    @SerializedName("previous") val previous: String?,
    @SerializedName("results") val results: List<T>
)

data class CreatePlanRequest(
    @SerializedName("title") val title: String,
    @SerializedName("description") val description: String?,
    @SerializedName("starts_at") val startsAt: String?,
    @SerializedName("ends_at") val endsAt: String?,
    @SerializedName("capacity") val capacity: Int?,
    @SerializedName("visibility") val visibility: String = "public"
)

data class Message(
    @SerializedName("id") val id: String,
    @SerializedName("plan") val planId: String,
    @SerializedName("user") val user: User?,
    @SerializedName("content") val content: String,
    @SerializedName("created_at") val createdAt: String
)
