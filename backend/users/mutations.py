"""Users schema."""


# Standard Library
import random
import re
import string

# Django
from django.utils.html import escape, strip_tags

# 3rd-Party
import graphene
from graphene import relay
from graphene_django import DjangoObjectType

# Local
from .models import User, UserVerification


class UserNode(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = User
        filter_fields = ["id"]
        interfaces = (relay.Node,)


#
class AddUser(graphene.Mutation):
    ok = graphene.Boolean()
    response = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=False)
        email = graphene.String(required=True)

    @staticmethod
    def password_validation(password: str) -> tuple[bool, str]:
        val = True
        response = "Everything is fine"

        if len(password) < 6:
            response = "length should be at least 6"
            val = False

        if not any(char.isdigit() for char in password):
            response = "Password should have at least one numeral"
            val = False

        if not any(char.islower() for char in password):
            response = "Password should have at least one lowercase letter"
            val = False

        return val, response

    @staticmethod
    def username_validation(username: str) -> bool:
        return True

    @staticmethod
    def email_validation(email: str) -> bool:
        regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        return True if re.search(regex, email) else False

    @staticmethod
    def mutate(root, info, **kwargs):  # type: ignore
        username = kwargs.get("username")
        password = kwargs.get("password")
        confirm_password = kwargs.get("confirm_password")
        email = kwargs.get("email")

        if not AddUser.username_validation(username):
            return AddUser(ok=False, response="Username already exists!")
        val, response = AddUser.password_validation(password)
        if not val:
            return AddUser(ok=False, response=response)
        if confirm_password != password:
            return AddUser(ok=False, response="Passwords do not match!")
        if not AddUser.email_validation(email):
            return AddUser(ok=False, response="Invalid email!")
        user = User(username=username, email=email, password=password)
        user.save()
        code = "".join(
            [
                random.SystemRandom().choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits
                )
                for n in range(10)
            ]
        )
        verification = UserVerification(
            user=user, verification_code=code, code_type="token"
        )
        verification.save()
        user.email_user(
            subject="Verification code",
            message=f"Your verification code {code}",
            fail_silently=None,
        )
        return AddUser(ok=True, response="Account created. Check your mailbox")


class VerifyUser(graphene.Mutation):
    ok = graphene.Boolean()
    response = graphene.String()

    class Arguments:
        id = graphene.ID()
        code = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):  # type: ignore
        code = kwargs.get("code")
        user = int(kwargs.get("id"))
        ver = UserVerification.objects.get(user=user)
        if ver.verify(code, "token"):
            ver.delete()
            return VerifyUser(ok=True, response="Account Activated.")
        else:
            return VerifyUser(ok=False, response="Something went wrong...")


class NewPassword(graphene.Mutation):
    ok = graphene.Boolean()
    response = graphene.String()

    class Arguments:
        email = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):  # type: ignore

        email = kwargs.get("email")
        if User.objects.get(email=email):
            user = User.objects.get(email=email)
            code = "".join(random.choice(string.ascii_letters) for i in range(10))
            verification = UserVerification(
                user=user, verification_code=code, code_type="password"
            )
            verification.save()
            user.email_user(
                subject="Password recovery",
                message="Here's your confirmation code: " + code,
                fail_silently=None,
            )
            return NewPassword(ok=True, response="Sending massage to your email!")
        else:
            return NewPassword(ok=False, response="No such email.")


class EditPassword(graphene.Mutation):
    ok = graphene.Boolean()
    response = graphene.String()

    class Arguments:
        email = graphene.String()
        code = graphene.String()
        new_password = graphene.String()
        confirm_new_password = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):  # type: ignore

        email = kwargs.get("email")
        code = kwargs.get("code")
        passw = kwargs.get("new_password")
        confirm_passw = kwargs.get("confirm_new_password")
        if User.objects.get(email=email):
            user = User.objects.get(email=email)
            userid = user.id
            if UserVerification.objects.get(user_id=userid):
                ver = UserVerification.objects.get(user_id=userid)
                if ver.verification_code == code:
                    if passw == confirm_passw:
                        setattr(user, "password", passw)
                        user.save()

            return EditPassword(ok=True, response="Password changed")
        else:
            return EditPassword(ok=False, response="Wrong mail")


class EditUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        description = graphene.String()
        password = graphene.String()

    def mutate(cls, info, id: graphene.ID, **kwargs):  # type: ignore
        # type: ignore
        user = User.objects.get(pk=id)
        for attr in kwargs.keys():
            value = kwargs.get(attr, getattr(user, attr))
            if attr == "description":
                setattr(user, attr, strip_tags(escape(value)))
            else:
                setattr(user, attr, value)
        user.save()
        return cls(ok=True, user=info.context.user)


class EditUserDescription(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        description = graphene.String()

    def mutate(cls, info, id: graphene.ID, **kwargs):  # type: ignore
        user = User.objects.get(pk=id)
        user.description = strip_tags(
            escape(kwargs.get("description", user.description))
        )
        user.save()
        return cls(ok=True, user=info.context.user)


class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(cls, info, id: graphene.ID, **kwargs):  # type: ignore
        user = User.objects.get(pk=id)
        user.delete()
        return cls(ok=True)


class UserMutation(graphene.ObjectType):
    add_user = AddUser.Field()
    verify_user = VerifyUser.Field()
    edit_user = EditUser.Field()
    edit_user_description = EditUserDescription.Field()
    delete_user = DeleteUser.Field()
    new_password = NewPassword.Field()
    edit_password = EditPassword.Field()
