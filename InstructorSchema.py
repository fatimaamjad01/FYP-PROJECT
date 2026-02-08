import strawberry
from prisma import Prisma
from typing import Optional
from fastapi import HTTPException
import typing
import bcrypt
import re
import datetime
import jwt
from datetime import timedelta


# Initialize Prisma client
db = Prisma()

# JWT configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def validate_password(password: str):
	if len(password) < 8:
		raise ValueError("Password must be at least 8 characters long")
	if not re.search(r"\d", password):
		raise ValueError("Password must contain at least one digit")
	if not re.search(r"[A-Za-z]", password):
		raise ValueError("Password must contain at least one letter")
	if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
		raise ValueError("Password must contain at least one special character")


def validate_email(email: str):
	if not re.match(email_regex, email):
		raise ValueError("Invalid email format")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
	else:
		expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


@strawberry.type
class Instructor:
	instructor_id: int
	first_name: str
	last_name: str
	email: str
	password: str
	phone_number: Optional[str]
	gender: Optional[str]
	dob: Optional[str]
	bio: Optional[str]
	profile_image: Optional[str]
	city: Optional[str]
	country: Optional[str]
	account_type: Optional[str]
	account_status: str
	qualification: Optional[str]
	expertise_area: Optional[str]
	year_of_experience: Optional[int]
	email_verified: bool
	last_login: Optional[str]
	password_last_change: Optional[str]
	created_at: str
	updated_at: str


@strawberry.type
class InstructorLoginResponse:
	token: str
	user: "InstructorUserInfo"


@strawberry.type
class InstructorUserInfo:
	instructor_id: int
	first_name: str
	last_name: str
	email: str
	role: str
	profile_image: Optional[str]


@strawberry.type
class InstructorPaginatedResponse:
	instructors: typing.List[Instructor]
	total_count: int
	filtered_count: int


@strawberry.type
class Course:
	course_id: int
	course_title: str
	course_description: Optional[str]
	course_thumbnail: Optional[str]
	course_level: Optional[str]
	course_language: Optional[str]
	meta_title: Optional[str]
	meta_description: Optional[str]
	meta_keywords: Optional[str]
	estimated_comp_time: Optional[int]
	course_duration: Optional[int]
	total_modules: int
	total_lectures: int
	total_videos: int
	total_resources: int
	course_status: str
	published_at: Optional[str]
	created_at: str
	updated_at: str


@strawberry.type
class CoursePaginatedResponse:
	courses: typing.List[Course]
	total_count: int
	filtered_count: int


@strawberry.input
class InstructorInput:
	first_name: str
	last_name: str
	email: str
	password: str
	phone_number: Optional[str] = None
	gender: Optional[str] = None
	dob: Optional[str] = None
	bio: Optional[str] = None
	profile_image: Optional[str] = None
	city: Optional[str] = None
	country: Optional[str] = None
	account_type: Optional[str] = None
	account_status: Optional[str] = None
	qualification: Optional[str] = None
	expertise_area: Optional[str] = None
	year_of_experience: Optional[int] = None
	email_verified: Optional[bool] = None


@strawberry.input
class CourseInput:
	course_title: str
	course_description: Optional[str] = None
	course_thumbnail: Optional[str] = None
	course_level: Optional[str] = None
	course_language: Optional[str] = None
	meta_title: Optional[str] = None
	meta_description: Optional[str] = None
	meta_keywords: Optional[str] = None
	estimated_comp_time: Optional[int] = None
	course_duration: Optional[int] = None
	total_modules: Optional[int] = None
	total_lectures: Optional[int] = None
	total_videos: Optional[int] = None
	total_resources: Optional[int] = None
	course_status: Optional[str] = None
	published_at: Optional[str] = None


@strawberry.type
class Query:
	@strawberry.field
	async def login_instructor(self, email: str, password: str) -> InstructorLoginResponse:
		try:
			instructor = await db.instructor.find_unique(where={"email": email})
			if not instructor:
				raise HTTPException(status_code=401, detail="Invalid email or password")
			if not bcrypt.checkpw(password.encode("utf-8"), instructor.password.encode("utf-8")):
				raise HTTPException(status_code=401, detail="Invalid email or password")

			# update last_login
			try:
				await db.instructor.update(
					where={"instructor_id": instructor.instructor_id},
					data={"last_login": datetime.datetime.now(datetime.timezone.utc).isoformat()},
				)
			except Exception as e:
				raise HTTPException(status_code=400, detail=f"Error updating last_login:{str(e)}")

			token_data = {
				"sub": str(instructor.instructor_id),
				"email": instructor.email,
				"first_name": instructor.first_name,
				"last_name": instructor.last_name,
				"role": "instructor",
			}
			access_token = create_access_token(data=token_data)

			user_info = InstructorUserInfo(
				instructor_id=instructor.instructor_id,
				first_name=instructor.first_name,
				last_name=instructor.last_name,
				email=instructor.email,
				role="instructor",
				profile_image=instructor.profile_image,
			)

			return InstructorLoginResponse(token=access_token, user=user_info)
		except HTTPException:
			raise
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

	@strawberry.field
	async def list_instructors(
		self,
		page: int = 1,
		per_page: int = 10,
		sort_field: str = "instructor_id",
		sort_order: str = "asc",
		search: typing.Optional[str] = None,
	) -> InstructorPaginatedResponse:
		if page < 1:
			page = 1
		if per_page < 1:
			per_page = 10
		skip = (page - 1) * per_page

		allowed_sort_fields = {
			"instructor_id",
			"first_name",
			"last_name",
			"email",
			"account_status",
			"created_at",
			"updated_at",
		}
		field = sort_field if sort_field in allowed_sort_fields else "instructor_id"
		direction = sort_order.lower() if sort_order.lower() in {"asc", "desc"} else "asc"
		order: typing.Optional[dict] = {field: direction}

		try:
			where_clause = {}
			if search:
				where_clause = {
					"OR": [
						{"first_name": {"contains": search, "mode": "insensitive"}},
						{"last_name": {"contains": search, "mode": "insensitive"}},
						{"email": {"contains": search, "mode": "insensitive"}},
					],
				}

			total_count = await db.instructor.count()
			filtered_count = await db.instructor.count(where=where_clause if where_clause else None)

			instructors = await db.instructor.find_many(
				where=where_clause if where_clause else None,
				skip=skip,
				take=per_page,
				order=order,
			)
			return InstructorPaginatedResponse(
				instructors=instructors,
				total_count=total_count,
				filtered_count=filtered_count,
			)
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

	@strawberry.field
	async def list_courses(
		self,
		page: int = 1,
		per_page: int = 10,
		sort_field: str = "course_id",
		sort_order: str = "asc",
		search: typing.Optional[str] = None,
	) -> CoursePaginatedResponse:
		if page < 1:
			page = 1
		if per_page < 1:
			per_page = 10
		skip = (page - 1) * per_page

		allowed_sort_fields = {
			"course_id",
			"course_title",
			"course_status",
			"created_at",
			"updated_at",
		}
		field = sort_field if sort_field in allowed_sort_fields else "course_id"
		direction = sort_order.lower() if sort_order.lower() in {"asc", "desc"} else "asc"
		order: typing.Optional[dict] = {field: direction}

		try:
			where_clause = {}
			if search:
				where_clause = {
					"OR": [
						{"course_title": {"contains": search, "mode": "insensitive"}},
						{"course_status": {"contains": search, "mode": "insensitive"}},
						{"course_level": {"contains": search, "mode": "insensitive"}},
						{"course_language": {"contains": search, "mode": "insensitive"}},
					],
				}

			total_count = await db.course.count()
			filtered_count = await db.course.count(where=where_clause if where_clause else None)

			courses = await db.course.find_many(
				where=where_clause if where_clause else None,
				skip=skip,
				take=per_page,
				order=order,
			)
			return CoursePaginatedResponse(
				courses=courses,
				total_count=total_count,
				filtered_count=filtered_count,
			)
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@strawberry.type
class Mutation:
	@strawberry.mutation
	async def register_instructor(self, input: InstructorInput) -> Instructor:
		try:
			validate_email(input.email)
			validate_password(input.password)

			existing = await db.instructor.find_unique(where={"email": input.email})
			if existing:
				raise ValueError(f"Email {input.email} is already registered")

			hashed = bcrypt.hashpw(input.password.encode("utf-8"), bcrypt.gensalt())
			instructor = await db.instructor.create(
				data={
					"first_name": input.first_name,
					"last_name": input.last_name,
					"email": input.email,
					"password": hashed.decode("utf-8"),
					"phone_number": input.phone_number if input.phone_number else None,
					"gender": input.gender,
					"dob": input.dob,
					"bio": input.bio,
					"profile_image": input.profile_image,
					"city": input.city,
					"country": input.country,
					"account_type": input.account_type,
					"account_status": input.account_status if input.account_status else "active",
					"qualification": input.qualification,
					"expertise_area": input.expertise_area,
					"year_of_experience": input.year_of_experience,
					"email_verified": input.email_verified if input.email_verified is not None else False,
				}
			)
			return instructor
		except ValueError as e:
			raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

	@strawberry.mutation
	async def update_instructor(self, instructor_id: int, input: InstructorInput) -> Instructor:
		try:
			validate_email(input.email)
			if input.password:
				validate_password(input.password)
				hashed = bcrypt.hashpw(input.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
			else:
				hashed = None

			existing = await db.instructor.find_unique(where={"instructor_id": instructor_id})
			if not existing:
				raise HTTPException(status_code=404, detail=f"Instructor with ID {instructor_id} not found")

			updated = await db.instructor.update(
				where={"instructor_id": instructor_id},
				data={
					"first_name": input.first_name if input.first_name is not None else existing.first_name,
					"last_name": input.last_name if input.last_name is not None else existing.last_name,
					"email": input.email if input.email is not None else existing.email,
					"phone_number": input.phone_number if input.phone_number is not None else existing.phone_number,
					"gender": input.gender if input.gender is not None else existing.gender,
					"dob": input.dob if input.dob is not None else existing.dob,
					"bio": input.bio if input.bio is not None else existing.bio,
					"profile_image": input.profile_image if input.profile_image is not None else existing.profile_image,
					"city": input.city if input.city is not None else existing.city,
					"country": input.country if input.country is not None else existing.country,
					"account_type": input.account_type if input.account_type is not None else existing.account_type,
					"account_status": input.account_status if input.account_status is not None else existing.account_status,
					"qualification": input.qualification if input.qualification is not None else existing.qualification,
					"expertise_area": input.expertise_area if input.expertise_area is not None else existing.expertise_area,
					"year_of_experience": input.year_of_experience if input.year_of_experience is not None else existing.year_of_experience,
					"email_verified": input.email_verified if input.email_verified is not None else existing.email_verified,
					"password": hashed if hashed else existing.password,
				},
			)
			return updated
		except ValueError as e:
			raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
		except HTTPException:
			raise
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

	@strawberry.mutation
	async def create_course(self, input: CourseInput) -> Course:
		try:
			data = {"course_title": input.course_title}
			if input.course_description is not None:
				data["course_description"] = input.course_description
			if input.course_thumbnail is not None:
				data["course_thumbnail"] = input.course_thumbnail
			if input.course_level is not None:
				data["course_level"] = input.course_level
			if input.course_language is not None:
				data["course_language"] = input.course_language
			if input.meta_title is not None:
				data["meta_title"] = input.meta_title
			if input.meta_description is not None:
				data["meta_description"] = input.meta_description
			if input.meta_keywords is not None:
				data["meta_keywords"] = input.meta_keywords
			if input.estimated_comp_time is not None:
				data["estimated_comp_time"] = input.estimated_comp_time
			if input.course_duration is not None:
				data["course_duration"] = input.course_duration
			if input.total_modules is not None:
				data["total_modules"] = input.total_modules
			if input.total_lectures is not None:
				data["total_lectures"] = input.total_lectures
			if input.total_videos is not None:
				data["total_videos"] = input.total_videos
			if input.total_resources is not None:
				data["total_resources"] = input.total_resources
			if input.course_status is not None:
				data["course_status"] = input.course_status
			if input.published_at is not None:
				data["published_at"] = input.published_at

			course = await db.course.create(data=data)
			return course
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

	@strawberry.mutation
	async def update_course(self, course_id: int, input: CourseInput) -> Course:
		try:
			existing = await db.course.find_unique(where={"course_id": course_id})
			if not existing:
				raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")

			updated = await db.course.update(
				where={"course_id": course_id},
				data={
					"course_title": input.course_title if input.course_title is not None else existing.course_title,
					"course_description": input.course_description if input.course_description is not None else existing.course_description,
					"course_thumbnail": input.course_thumbnail if input.course_thumbnail is not None else existing.course_thumbnail,
					"course_level": input.course_level if input.course_level is not None else existing.course_level,
					"course_language": input.course_language if input.course_language is not None else existing.course_language,
					"meta_title": input.meta_title if input.meta_title is not None else existing.meta_title,
					"meta_description": input.meta_description if input.meta_description is not None else existing.meta_description,
					"meta_keywords": input.meta_keywords if input.meta_keywords is not None else existing.meta_keywords,
					"estimated_comp_time": input.estimated_comp_time if input.estimated_comp_time is not None else existing.estimated_comp_time,
					"course_duration": input.course_duration if input.course_duration is not None else existing.course_duration,
					"total_modules": input.total_modules if input.total_modules is not None else existing.total_modules,
					"total_lectures": input.total_lectures if input.total_lectures is not None else existing.total_lectures,
					"total_videos": input.total_videos if input.total_videos is not None else existing.total_videos,
					"total_resources": input.total_resources if input.total_resources is not None else existing.total_resources,
					"course_status": input.course_status if input.course_status is not None else existing.course_status,
					"published_at": input.published_at if input.published_at is not None else existing.published_at,
				},
			)
			return updated
		except HTTPException:
			raise
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
